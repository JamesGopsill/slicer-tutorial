import vtk
import pyx


def interior(cut_polys, n: int, spacing=0.1):
	""" This function will create the interior shells for a component. """

	shells_int = []

	n_cells = cut_polys.GetNumberOfCells()
	poly = cut_polys.GetCell(0)

	# If there are more than one polys from the cutter
	if n_cells != 1:

		# Run through each poly that has been generated
		for i in range(1, cut_polys.GetNumberOfCells()):

			# Update poly if the next one is smaller
			if cut_polys.GetCell(i).ComputeArea() > poly.ComputeArea():
				poly = cut_polys.GetCell(i)

	
	
	# get the initial line
	from_x, from_y, _ = poly.GetEdge(0).GetPoints().GetData().GetTuple(0)
	to_x, to_y, _ = poly.GetEdge(0).GetPoints().GetData().GetTuple(1)

	# Add line to start the shell
	shell = pyx.path.line(from_x, from_y, to_x, to_y)

	# run through the remaining polys
	for j in range(1, poly.GetNumberOfEdges()):

		# Extend the line
		to_x, to_y, _ = poly.GetEdge(j).GetPoints().GetData().GetTuple(1)

		# Append to the shell
		shell.append(pyx.path.lineto(to_x, to_y))

	# Append the shell to the list
	shells_int.append(shell)

	# Now deform the path to add the additional shells
	#if n != 0:
	#	for i in range(1, n):
	#		shells_int.append(pyx.deformer.parallel(i * -spacing,dointersection=1).deform(shell))

	return shells_int
