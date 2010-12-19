import java.util.EnumMap;

import pushpuzzle.creator.PushCreator;
import pushpuzzle.player.PushPlayer;


import solver.gui.PuzzleMode;
import solver.plugin.IPuzzlePane;
import solver.plugin.IPuzzleType;

public class PushPuzzle implements IPuzzleType
{
	private EnumMap<PuzzleMode, IPuzzlePane> panes;
	
	public PushPuzzle()
	{
		panes = new EnumMap<PuzzleMode, IPuzzlePane>(PuzzleMode.class);
	}
	
	public String getType()
	{
		return "Sun's Push Puzzle";
	}
	
	public IPuzzlePane get(PuzzleMode mode)
	{
		if(panes.get(mode) == null)
		{
			switch(mode)
			{
				case CREATE:
					panes.put(mode, new PushCreator());
					break;
				case PLAY:
					panes.put(mode, new PushPlayer());
					break;
			}
		}
		
		return panes.get(mode);
	}
}