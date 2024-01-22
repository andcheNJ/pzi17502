using static PowerSupplyModule.PowerSupply;

namespace PowerSupplyModule
{
    /// <summary>
    /// Exception for general PowerSupply errors
    /// </summary>
   
    public class PowerSupplyNotConnectedException : System.Exception
    {
        public PowerSupplyState Status { get; private set; }

        public PowerSupplyNotConnectedException()
        {
        }

        public PowerSupplyNotConnectedException(string message)
            : base(message)
        {
        }

        public PowerSupplyNotConnectedException(string message, PowerSupplyState status)
            : base(message)
        {
            Status = status;
        }
    }

    public class PowerSupplyConnectionFailedException : System.Exception
    {
        public PowerSupplyState Status { get; private set; }

        public PowerSupplyConnectionFailedException()
        {
        }

        public PowerSupplyConnectionFailedException(string message)
            : base(message)
        {
        }

        public PowerSupplyConnectionFailedException(string message, PowerSupplyState status)
            : base(message)
        {
            Status = status;
        }
    }

    public class PowerSupplyNotReadyException : System.Exception
    {
        public PowerSupplyState Status { get; private set; }

        public PowerSupplyNotReadyException()
        {
        }

        public PowerSupplyNotReadyException(string message)
            : base(message)
        {
        }

        public PowerSupplyNotReadyException(string message, PowerSupplyState status)
            : base(message)
        {
            Status = status;
        }
    }

    public class PowerSupplyTCPException : System.Exception
    {
        public PowerSupplyState Status { get; private set; }

        public PowerSupplyTCPException()
        {
        }

        public PowerSupplyTCPException(string message)
            : base(message)
        {
        }

        public PowerSupplyTCPException(string message, PowerSupplyState status)
            : base(message)
        {
            Status = status;
        }
    }

    public class PowerSupplyBackgroundWorkerException : System.Exception
    {
        public PowerSupplyState Status { get; private set; }

        public PowerSupplyBackgroundWorkerException()
        {
        }

        public PowerSupplyBackgroundWorkerException(string message)
            : base(message)
        {
        }

        public PowerSupplyBackgroundWorkerException(string message, PowerSupplyState status)
            : base(message)
        {
            Status = status;
        }
    }
}
