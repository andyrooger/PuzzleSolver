package pushpuzzle.creator;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.Window;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;

import solver.utility.Dimensions;

public class SizePicker extends JDialog implements ActionListener
{
	public static final long serialVersionUID = 1;
	
	private JTextField rows, cols;
	
	public SizePicker(Window parent)
  {
		super(parent, "Creating New Puzzle", ModalityType.APPLICATION_MODAL);
		
		if (parent != null)
		{
      Dimension parentSize = parent.getSize(); 
      Point p = parent.getLocation(); 
      setLocation(p.x + parentSize.width / 4, p.y + parentSize.height / 4);
    }
		
		JPanel content = new JPanel();
		content.setLayout(new BorderLayout());
		
		content.add(new JLabel("Choose a size for the play area"), BorderLayout.NORTH);
		
		JPanel input = new JPanel();
		input.setLayout(new GridLayout(2, 2));
		input.add(new JLabel("Rows: "));
		rows = new JTextField("10");
		input.add(rows);
		input.add(new JLabel("Cols: "));
		cols = new JTextField("10");
		input.add(cols);
		content.add(input, BorderLayout.CENTER);
		
		JButton ok = new JButton("OK");
		ok.addActionListener(this);
		content.add(ok, BorderLayout.SOUTH);
		
		content.setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
		getContentPane().add(content);

		pack();
		setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
		setVisible(true);
  }
	
	public void chosen(Dimensions d)
	{
	}
	
  public void actionPerformed(ActionEvent e)
  {
  	int irows, icols;
  	try
  	{
  		irows = Integer.parseInt(rows.getText().trim());
  		icols = Integer.parseInt(cols.getText().trim());
  	}
  	catch(NumberFormatException ex)
  	{
  		JOptionPane.showMessageDialog(this,
			        "Rows and columns both need to be positive whole numbers.",
			        "Whoops", JOptionPane.ERROR_MESSAGE);
  		return;
  	}
  	
  	if(irows < 1 || icols < 1)
  		JOptionPane.showMessageDialog(this,
			        "Rows and columns both need to be positive whole numbers.",
			        "Whoops", JOptionPane.ERROR_MESSAGE);
  	
  	chosen(new Dimensions(irows, icols));
  	setVisible(false);
  	dispose();
  }
}
