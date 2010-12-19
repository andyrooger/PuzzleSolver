package pushpuzzle.solver;

import java.awt.BorderLayout;
import java.awt.Frame;
import java.awt.Insets;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

public class ProgressDialog extends JDialog
{
	public static final long serialVersionUID = 1;
	
	protected JTextArea output;
	protected JProgressBar progress;
	
	public ProgressDialog(Frame parent, ActionListener onCancel, int maxmoves)
	{
		super(parent, "Solving...", true);
		
		setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
		
		setLayout(new BorderLayout());
		
		progress = new JProgressBar(0, maxmoves);
		progress.setValue(0);
		progress.setStringPainted(true);
		
		add(progress, BorderLayout.NORTH);
		
		output = new JTextArea(5, 20);
		output.setMargin(new Insets(5,5,5,5));
    output.setEditable(false);
    output.setLineWrap(true);
    output.setWrapStyleWord(true);
    
    add(new JScrollPane(output), BorderLayout.CENTER);
		
		JButton cancel = new JButton("Cancel");
		cancel.addActionListener(onCancel);
		
		add(cancel, BorderLayout.SOUTH);
		
		pack();
	}
	
	public void addStatus(String status)
	{
		output.append(status+'\n');
	}
	
	public void movesLeft(int moves)
	{
		progress.setValue(progress.getMaximum() - moves);
		progress.setString("Approx moves left: " + moves);
	}
}