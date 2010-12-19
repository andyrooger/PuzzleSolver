package pushpuzzle.solver;

import java.awt.Frame;
import java.awt.event.ActionListener;

public class WeightedProgressDialog extends ProgressDialog
{
	public static final long serialVersionUID = 1;
	public static final int weight = 8;
	
	protected int initialMoves;
	public WeightedProgressDialog(Frame parent, ActionListener onCancel, int maxmoves, int initialMoves)
	{
		super(parent, onCancel, (maxmoves-initialMoves)/weight + (initialMoves));
		this.initialMoves = initialMoves;
	}
	
	public void movesLeft(int moves)
	{
		if(moves > initialMoves)
			super.movesLeft(moves/weight);
		else
			super.movesLeft(moves);
	}
}
