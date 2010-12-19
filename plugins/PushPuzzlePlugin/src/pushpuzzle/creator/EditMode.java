package pushpuzzle.creator;

public enum EditMode
{
	EMPTY,
	WALL,
	TARGET,
	BOX,
	PLAYER;
	
	public String toString()
	{
		String lower = super.toString();
		return lower.substring(0, 1).toUpperCase() + lower.substring(1).toLowerCase();
	}
}
