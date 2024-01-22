
namespace DiagnosticModule
{
    
    public class EdiabasNotReadyException : System.Exception
    {
        public EdiabasSingleton.EdiabasState Status { get; private set; }

        public EdiabasNotReadyException()
        {
        }

        public EdiabasNotReadyException(string message)
            : base(message)
        {
        }

        public EdiabasNotReadyException(string message, EdiabasSingleton.EdiabasState status)
            : base(message)
        {
            Status = status;
        }
    }

    public class EdiabasInitialiseFailedException : System.Exception
    {
        public EdiabasSingleton.EdiabasState Status { get; private set; }

        public EdiabasInitialiseFailedException()
        {
        }

        public EdiabasInitialiseFailedException(string message)
            : base(message)
        {
        }

        public EdiabasInitialiseFailedException(string message, EdiabasSingleton.EdiabasState status)
            : base(message)
        {
            Status = status;
        }
    }

  
}
