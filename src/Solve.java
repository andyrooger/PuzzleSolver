import javax.swing.SwingUtilities;

import solver.gui.*;

public class Solve
{
	public static void main(String[] args)
	{
		if(args.length == 1)
		{
			final String arg = args[0];
			SwingUtilities.invokeLater(new Runnable()
			{
				public void run()
				{
					new SolverGUI(arg);
				}
			});
		}
		else
			System.out.println("Usage: java Solve path");
	}
}
