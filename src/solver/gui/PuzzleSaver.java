package solver.gui;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.ObjectStreamClass;

import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.filechooser.FileFilter;

import solver.plugin.IPuzzle;
import solver.plugin.IPuzzlePane;

public class PuzzleSaver
{
	IPuzzlePane puzzle;
	
	public PuzzleSaver(IPuzzlePane puzzle)
	{
		this.puzzle = puzzle;
	}
	
	public boolean check(JFrame frame)
	{
		if(!puzzle.changed())
			return true;
		else
		{
			int choice = JOptionPane.showConfirmDialog(frame,
							"Looks like you've changed things and not saved, do you want to now?",
							"I'm helping you",
							JOptionPane.YES_NO_CANCEL_OPTION,
							JOptionPane.WARNING_MESSAGE);
			
			if(choice == JOptionPane.YES_OPTION)
				return save(frame);
			else
				return (choice == JOptionPane.NO_OPTION);
		}
	}
	
	public boolean save(JFrame frame)
	{
		if(puzzle.getPuzzle() == null)
		{
			JOptionPane.showMessageDialog(frame,
							"Sorry, this puzzle isn't saveable",
							"Whoops",
							JOptionPane.INFORMATION_MESSAGE);
			return false;
		}
		JFileChooser f = new JFileChooser();
		f.setFileFilter(new PuzzleFileFilter(puzzle.getExt()));
		
		int choice = f.showSaveDialog(frame);
		if(choice != JFileChooser.APPROVE_OPTION)
			return false;
		
		boolean goneWell = true;
		ObjectOutputStream o = null;
		try
		{
			File sfile = f.getSelectedFile();
			String fname = sfile.getAbsolutePath();
			if(!fname.endsWith("."+puzzle.getExt()))
			{
				fname += "."+puzzle.getExt();
				sfile = new File(fname);
			}
			o = new ObjectOutputStream(new FileOutputStream(sfile));
			o.writeObject(puzzle.getPuzzle());
		}
		catch(FileNotFoundException e)
		{
			goneWell = false;
			JOptionPane.showMessageDialog(frame,
							"Looks like the file you chose cannot be created",
							"Whoops",
							JOptionPane.ERROR_MESSAGE);
		}
		catch(IOException e)
		{
			goneWell = false;
			JOptionPane.showMessageDialog(frame,
							"Something went wrong while writing your puzzle",
							"Whoops",
							JOptionPane.ERROR_MESSAGE);
		}
		finally
		{
			try
			{
				if(o != null)
					o.close();
			}
			catch(IOException e)
			{
				goneWell = false;
				JOptionPane.showMessageDialog(frame,
								"There was a problem while writing your puzzle",
								"Whoops",
								JOptionPane.ERROR_MESSAGE);
			}
		}
		
		if(goneWell)
			puzzle.saved();
		return goneWell;
	}
	
	public boolean load(JFrame frame)
	{
		if(puzzle.getExt() == null)
		{
			JOptionPane.showMessageDialog(frame,
							"Sorry, this puzzle isn't loadable",
							"Whoops",
							JOptionPane.INFORMATION_MESSAGE);
			return false;
		}
		JFileChooser f = new JFileChooser();
		f.setFileFilter(new PuzzleFileFilter(puzzle.getExt()));
		int choice = f.showOpenDialog(frame);
		if(choice != JFileChooser.APPROVE_OPTION)
			return false;
		
		boolean goneWell = true;
		IPuzzle p = null;
		ObjectInputStream i = null;
		try
		{
			i = new ObjectInputStream(new FileInputStream(f.getSelectedFile()))
			{
				protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException
		    {
					Class<?> c = null;
					c = Class.forName(desc.getName(), true, puzzle.getClass().getClassLoader());
					return c;
		    }
			};
			Object o = i.readObject();
			p = (IPuzzle)o;
		}
		catch(FileNotFoundException e)
		{
			goneWell = false;
			JOptionPane.showMessageDialog(frame,
							"Looks like the file you chose cannot be found",
							"Whoops",
							JOptionPane.ERROR_MESSAGE);
		}
		catch(IOException e)
		{
			goneWell = false;
			JOptionPane.showMessageDialog(frame,
							"Something went wrong while opening your puzzle",
							"Whoops",
							JOptionPane.ERROR_MESSAGE);
		}
		catch(ClassNotFoundException e)
		{
			System.out.println("Mucked it");
			e.printStackTrace();
			goneWell = false;
			JOptionPane.showMessageDialog(frame,
							"This is not a valid puzzle file",
							"Whoops",
							JOptionPane.ERROR_MESSAGE);
		}
		finally
		{
			try
			{
				if(i != null)
					i.close();
			}
			catch(IOException e)
			{
				goneWell = false;
				JOptionPane.showMessageDialog(frame,
								"There was a problem while opening your puzzle",
								"Whoops",
								JOptionPane.ERROR_MESSAGE);
			}
		}
		
		if(goneWell)
			return puzzle.load(p);
		
		return goneWell;
	}
	
	private class PuzzleFileFilter extends FileFilter
	{
		private String ext;
		
		public PuzzleFileFilter(String ext)
		{
			this.ext = ext;
		}
		
    public boolean accept(File f)
    {
	    return f.isFile() && f.getName().endsWith("."+ext);
    }

    public String getDescription()
    {
	    return "Puzzle file (*."+ext+")";
    }
	}
}
