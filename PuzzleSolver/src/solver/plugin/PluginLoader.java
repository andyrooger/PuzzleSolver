package solver.plugin;

import java.io.File;
import java.io.FilenameFilter;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.SwingWorker;

public abstract class PluginLoader
{
	private String baseDir;
	
	protected abstract void perPlugin(IPuzzleType p);
	
	public PluginLoader(String dir)
	{
		baseDir = dir;
	}
	
	// Find plugin directory, null if none
	private File checkDir(JFrame frame)
	{
		File base = new File(baseDir);
		if(!base.exists() || !base.isDirectory())
		{
			JOptionPane.showMessageDialog(frame,
			        "The base directory does not exist, cannot load plugins!",
			        "Whoops", JOptionPane.ERROR_MESSAGE);
			return null;
		}

		File pluginDir = null;
		for(File f : base.listFiles())
			if("plugin".equals(f.getName()))
			{
				pluginDir = f;
				break;
			}
		
		if(pluginDir == null)
		{
			JOptionPane.showMessageDialog(frame,
			        "The plugin directory does not exist, cannot load plugins!",
			        "Whoops", JOptionPane.ERROR_MESSAGE);
		}
		
		return pluginDir;
	}
	
	public void loadPlugins(final JFrame frame)
	{
		(new SwingWorker<Void, IPuzzleType>()
		{
      protected Void doInBackground() throws Exception
      {
	      File pluginDir = checkDir(frame);
	      if(pluginDir != null)
	      {
	      	for(File plugin : pluginDir.listFiles(new JarFilter()))
						loadPlugin(frame, plugin);
	      }
	      return null;
      }
      
      protected void process(List<IPuzzleType> chunks)
      {
      	for(IPuzzleType p : chunks)
      		perPlugin(p);
      }
		}).execute();
	}
	
	private void loadPlugin(JFrame frame, File f)
	{
		URL[] urls = new URL[1];
		urls[0] = null;
		try
		{
			urls[0] = new URL("file:///"+f.getAbsolutePath());
		}
		catch(MalformedURLException e)
		{
			JOptionPane.showMessageDialog(frame, "The plugin at "
			        + f.getAbsolutePath() + " could not be found.", "Whoops",
			        JOptionPane.ERROR_MESSAGE);
			return;
		}
		
		if(urls[0] != null)
		{
			ClassLoader loader = new URLClassLoader(urls);
			
			// Plugins with the main class PuzzleType are in jar file PuzzleType.jar
			String className = f.getName();
			className = className.substring(0, className.lastIndexOf("."));
			Class<?> c;
			try
			{
				c = loader.loadClass(className);
			}
			catch(ClassNotFoundException e)
			{
				JOptionPane.showMessageDialog(frame, "Could not open plugin "
				        + className, "Whoops", JOptionPane.ERROR_MESSAGE);
				return;
			}
			
			IPuzzleType p = null;
			
			try
			{
				p = (IPuzzleType)c.newInstance();
			}
			catch(IllegalAccessException e)
			{
				JOptionPane.showMessageDialog(frame, "Could not start plugin "
				        + className, "Whoops", JOptionPane.ERROR_MESSAGE);
				return;
			}
			catch(InstantiationException e)
			{
				JOptionPane.showMessageDialog(frame, "Could not start plugin "
				        + className, "Whoops", JOptionPane.ERROR_MESSAGE);
				return;
			}
			
			if(p != null)
				perPlugin(p);
		}
	}
	
	private class JarFilter implements FilenameFilter
	{
		public boolean accept(File dir, String name)
		{
			// Accepts stuff in the plugin directory
			if(!"plugin".equals(dir.getName()))
				return false;
			
			// Ends in .jar
			return name.endsWith(".jar");
		}
	}
	
}
