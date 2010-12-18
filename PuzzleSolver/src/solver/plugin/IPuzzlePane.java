package solver.plugin;

import javax.swing.JPanel;

import solver.gui.SolverButton;

public interface IPuzzlePane
{
	public JPanel getPanel(); // gets the panel object
	public boolean start(IPuzzle p); // inits (p null if clean start, otherwise will return load p)
	public boolean load(IPuzzle puzzle); //Loads a puzzle returns success
	public IPuzzle getPuzzle(); // Returns the puzzle object if it is saveable or null otherwise
	public void saved(); // resets changed
	public boolean changed(); // returns the pane has been changed since saved() was called
	public void clean(); // Cleans whatever the user has done on the panel
	public ISolver getSolver(SolverButton btn); // Get a solver object related to the button btn
	public void end(); // Actually kills the panel
	public String getExt(); // Extension for the puzzle files, null indicates it cannot be loaded
}
