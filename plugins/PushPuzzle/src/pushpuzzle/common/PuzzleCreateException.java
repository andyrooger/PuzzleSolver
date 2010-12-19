package pushpuzzle.common;

public class PuzzleCreateException extends Exception
{
	public static final long serialVersionUID = 1;
	
	public PuzzleCreateException()
  {
	  super();
  }

	public PuzzleCreateException(String message, Throwable cause)
  {
	  super(message, cause);
  }

	public PuzzleCreateException(String message)
  {
	  super(message);
  }

	public PuzzleCreateException(Throwable cause)
  {
	  super(cause);
  }
	
}
