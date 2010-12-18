package solver.utility;

import java.io.Serializable;


public class BoolMap implements Serializable
{
	public static final long serialVersionUID = 1;
	
	private boolean[][] map;
	private final Dimensions dims;
	private final boolean def;
	
	public BoolMap(Dimensions d, boolean b)
	{
		dims = d;
		def = b;
		
		map = new boolean[d.getCols()][d.getRows()];
		for(int i=0; i<d.getCols(); i++)
			for(int j=0; j<d.getRows(); j++)
				map[i][j] = b;
	}
	
	public void set(Coords c, boolean b)
	{
		if(dims.contains(c))
			map[c.getCol()][c.getRow()] = b;
	}
	
	public boolean get(Coords c)
	{
		if(dims.contains(c))
			return map[c.getCol()][c.getRow()];
		else
			return def;
	}
	
	public Dimensions dims()
	{
		return dims;
	}
}
