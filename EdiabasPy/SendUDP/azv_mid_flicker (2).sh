#!/bin/bash

. color_print.sh
traperr() {
	bgred "ERROR: ${BASH_SOURCE[1]} at line ${BASH_LINENO[0]}"
}

trapint() {
	fgyellow "exiting ${BASH_SOURCE[1]}"
	if ps -C ffmpeg > /dev/null ; then
		killall -INT ffmpeg
		sleep 1
	fi
	exit 0
}

BCP_IP="169.254.22.84"
ECU_IP="169.254.192.41"
WORKDIR="/grmn/prj/aoem/mgu22/dlt-logs/azvmidflicker_repro/lg_eng_fw_2nd_round"
TARGET=redkit

trap traperr ERR
trap trapint INT

function sendhsfz {
	/grmn/prj/aoem/mgu22/out-of-tree/ascgit475.lsmf/tools/hsfz-send/sendhsfz.py --ecu 0x63 --server "${ECU_IP}" "${@}"
}

function sendpwf {
	/grmn/prj/aoem/mgu22/out-of-tree/ascgit475.lsmf/tools/hsfz-send/sendhsfz.py --ip-addr="$BCP_IP" --diag-addr 16 31 01 10 31 "${@}"
}

function set_cid_brightness_to_max {
	sendhsfz 31 01 f0 17 00 03 2e 01 64
}

function set_cid_brightness_to_min {
	sendhsfz 31 01 f0 17 00 03 2e 01 01
}

function print_status {
	echo -ne "[$(date +%H:%M:%S)] : ${*}\n"
}

function stop_ffmpeg {
	if ps -C ffmpeg > /dev/null ; then
		killall -INT ffmpeg
		sleep 1
	fi
}

function assure_devvideo0_is_free {
	if ps -C cheese > /dev/null ; then
		killall -KILL cheese
		sleep 1
	fi
	if ps -C ffmpeg > /dev/null ; then
		killall -INT ffmpeg
		sleep 1
	fi
}

delay=20
i=0
CURRENT_ERROR=0
FORMER_ERROR=0
ITERATION_TIMESTAMP=""
cd "$WORKDIR" || mkdir -p "$WORKDIR"
touch "$WORKDIR/reproductions.txt"
touch "$WORKDIR/ffmpeg_report.txt"
while true; do
	ITERATION_TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

	echo -ne "[$(date '+%H:%M:%S')] : $ITERATION_TIMESTAMP "
	bgyellow "  $i  "

	sendpwf 05 05 73 > /dev/null # whn
	print_status "wohnen -> $delay sec delay"
	sleep $delay

	sendpwf 03 03 88 > /dev/null # stnd
	print_status "stand -> 15 sec delay"
	sleep 15

	print_status "stopping ffmpeg -> 20 sec delay"
	stop_ffmpeg
	sleep 20

	print_status "starting ffmpeg -> 1 sec delay"
	assure_devvideo0_is_free
	ffmpeg -f v4l2 -i /dev/video4 -t 00:04:00 -vf "drawtext=text='%{localtime}':x=10:y=10:fontsize=26:fontcolor=white" -vcodec libx264 Flicker_${i}_"$ITERATION_TIMESTAMP".mp4 >> ffmpeg_report.txt 2>&1 &
	sleep 1
	# rack-start-stop
	sendpwf 05 05 73 > /dev/null # whn
	print_status "wohnen"
	sleep 1
	set_cid_brightness_to_min > /dev/null 2>&1 &
	# set_cid_brightness_to_max > /dev/null 2>&1 &
	sleep $((delay-1))

	sendpwf 07 07 d1 > /dev/null # prfad
	print_status "pad"
	((i+=1))
	sleep $delay

	CURRENT_ERROR=$(rg -ac '(FIFO-Underflow|SYNC-Stat-Error)(\. Value in FgChStat-Register| not present anymore)' "$WORKDIR"/azvmidflicker_repro.dlt || echo 0 )
	# print_status "CURRENT_ERROR: $CURRENT_ERROR | FORMER_ERROR: $FORMER_ERROR"
	if [[ $((CURRENT_ERROR-FORMER_ERROR)) -gt 7 ]]; then
		echo -ne "[$(date '+%H:%M:%S')] : $ITERATION_TIMESTAMP "
		bggreen " Reproduction "
		echo "[$(date '+%H:%M:%S')] : Record: Flicker_${i}_${ITERATION_TIMESTAMP}.mp4" >> "$WORKDIR"/reproductions.txt
		scp /mnt/s/tmp/reg_dumps.sh "$TARGET":/tmp/
		ssh "$TARGET" "mount -o remount,exec /tmp && /tmp/reg_dumps.sh" >> "$WORKDIR"/reproductions.txt
		echo "CURRENT_ERROR: $CURRENT_ERROR | FORMER_ERROR: $FORMER_ERROR" | tee -a "$WORKDIR"/reproductions.txt
		warn_remote
		warn_mobile
		# give more time for video
		sleep 10
		# stop video
		assure_devvideo0_is_free
		# stop in flickering state
		# exit
	fi
	FORMER_ERROR="$CURRENT_ERROR"
done
