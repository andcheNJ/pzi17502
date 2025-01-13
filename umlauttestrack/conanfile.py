from conans import ConanFile


class PackageLibraryConan(ConanFile):
    name = "ecutest.lib.umlautrackcontrol"
    version = "1.0.1"
    author = "TraceTronic"
    description = "ECU-TEST library workspace for functions related to Umlaut Rack Control"
    default_channel = "release"
    default_user = "tracetronic"

    scm = {"revision": "715b460dc114bdb2247eca1795001f31c1b73596",
           "type": "git",
           "url": "git@cc-github.bmwgroup.net:IuK-Testautomation/ecutest.lib.umlautrackcontrol.git"}

    def build(self):
        pass

    def package(self):
        self.copy("*", src="", dst="", excludes=('*_Test', 'zuul.d', 'conan_upload.exe.lnk'))
