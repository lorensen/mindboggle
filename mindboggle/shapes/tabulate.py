#!/usr/bin/env python
"""
Functions for writing tables


Authors:
    - Arno Klein, 2012-2013  (arno@mindboggle.info)  http://binarybottle.com

Copyright 2013,  Mindboggle team (http://mindboggle.info), Apache v2.0 License

"""

def write_mean_shapes_tables(labels_or_file, sulci=[], fundi=[],
        area_file='', depth_file='', mean_curvature_file='',
        gauss_curvature_file='', max_curvature_file='', min_curvature_file='',
        thickness_file='', convexity_file='',
        labels_spectra=[], labels_spectra_norm=[], labels_spectra_IDs=[],
        sulci_spectra=[], sulci_spectra_norm=[], sulci_spectra_IDs=[],
        exclude_labels=[-1], delimiter=','):
    """
    Make tables of mean shape values per label, fundus, and/or sulcus.

    Parameters
    ----------
    labels_or_file : list or string
        label number for each vertex or name of VTK file with index scalars
    sulci :  list of integers
        indices to sulci, one per vertex, with -1 indicating no sulcus
    fundi :  list of integers
        indices to fundi, one per vertex, with -1 indicating no fundus
    area_file :  string
        name of VTK file with scalar surface area values
    depth_file :  string
        name of VTK file with scalar depth values
    mean_curvature_file :  string
        name of VTK file with scalar mean curvature values
    gauss_curvature_file :  string
        name of VTK file with scalar Gaussian curvature values
    max_curvature_file :  string
        name of VTK file with scalar maximum curvature values
    min_curvature_file :  string
        name of VTK file with scalar minimum curvature values
    thickness_file :  string
        name of VTK file with scalar thickness values
    convexity_file :  string
        name of VTK file with scalar convexity values
    labels_spectra : list of lists of floats
        Laplace-Beltrami spectra for labeled regions
    labels_spectra_norm : list of lists of floats
        Laplace-Beltrami spectra for labeled regions normalized by area
    labels_spectra_IDs : list of integers
        unique ID numbers (labels) for labels_spectra
    sulci_spectra : list of lists of floats
        Laplace-Beltrami spectra for sulci
    sulci_spectra_norm : list of lists of floats
        Laplace-Beltrami spectra for sulci normalized by area
    sulci_spectra_IDs : list of integers
        unique ID numbers (labels) for sulci_spectra
    exclude_labels : list of lists of integers
        indices to be excluded (in addition to -1)
    delimiter : string
        delimiter between columns, such as ','

    Returns
    -------
    label_table :  string
        output table filename for label shapes
    sulcus_table :  string
        output table filename for sulcus shapes
    fundus_table :  string
        output table filename for fundus shapes
    norm_label_table :  string
        output table filename for label shapes normalized by area
    norm_sulcus_table :  string
        output table filename for sulcus shapes normalized by area
    norm_fundus_table :  string
        output table filename for fundus shapes normalized by area

    Examples
    --------
    >>> import os
    >>> from mindboggle.utils.io_vtk import read_scalars
    >>> from mindboggle.shapes.tabulate import write_mean_shapes_tables
    >>> path = os.environ['MINDBOGGLE_DATA']
    >>> labels_or_file = os.path.join(path, 'arno', 'labels', 'lh.labels.DKT25.manual.vtk')
    >>> sulci_file = os.path.join(path, 'arno', 'features', 'sulci.vtk')
    >>> fundi_file = os.path.join(path, 'arno', 'features', 'fundi.vtk')
    >>> sulci, name = read_scalars(sulci_file)
    >>> fundi, name = read_scalars(fundi_file)
    >>> area_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.area.vtk')
    >>> depth_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.depth.vtk')
    >>> mean_curvature_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.curv.avg.vtk')
    >>> gauss_curvature_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.curv.gauss.vtk')
    >>> max_curvature_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.curv.max.vtk')
    >>> min_curvature_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.curv.min.vtk')
    >>> thickness_file = ''
    >>> convexity_file = ''
    >>> delimiter = ','
    >>> #
    >>> import numpy as np
    >>> labels, name = read_scalars(labels_or_file)
    >>> labels_spectra = [[1,2,3] for x in labels]
    >>> labels_spectra_norm = [[1,2,3] for x in labels]
    >>> labels_spectra_IDs = np.unique(labels).tolist()
    >>> sulci_spectra = [[1,2,3] for x in sulci]
    >>> sulci_spectra_norm = [[1,2,3] for x in sulci]
    >>> sulci_spectra_IDs = np.unique(sulci).tolist()
    >>> exclude_labels = [-1]
    >>> #
    >>> write_mean_shapes_tables(labels_or_file, sulci, fundi, \
    >>>     area_file, depth_file, mean_curvature_file, \
    >>>     gauss_curvature_file, max_curvature_file, min_curvature_file, \
    >>>     thickness_file, convexity_file, labels_spectra,
    >>>     labels_spectra_norm, labels_spectra_IDs, sulci_spectra, \
    >>>     sulci_spectra_norm, sulci_spectra_IDs, exclude_labels, delimiter)

    """
    import os
    import numpy as np
    from mindboggle.shapes.measure import mean_value_per_label
    from mindboggle.utils.io_vtk import read_scalars
    from mindboggle.utils.io_file import write_columns

    # Make sure inputs are lists:
    if isinstance(labels_or_file, np.ndarray):
        labels = labels_or_file.tolist()
    elif isinstance(labels_or_file, list):
        labels = labels_or_file
    elif isinstance(labels_or_file, str):
        labels, name = read_scalars(labels_or_file)
    if isinstance(sulci, np.ndarray):
        sulci = sulci.tolist()
    if isinstance(fundi, np.ndarray):
        fundi = fundi.tolist()

    # Feature lists:
    feature_lists = [labels, sulci, fundi]
    spectra_lists = [labels_spectra, sulci_spectra]
    spectra_norm_lists = [labels_spectra_norm, sulci_spectra_norm]
    spectra_ID_lists = [labels_spectra_IDs, sulci_spectra_IDs]
    spectra_names = ['label_spectrum', 'sulcus_spectrum']
    table_names = ['label_shapes.csv', 'sulcus_shapes.csv', 'fundus_shapes.csv']

    # Shape names corresponding to shape files below:
    shape_names = ['area', 'depth', 'mean_curvature', 'gauss_curvature',
                   'max_curvature', 'min_curvature', 'thickness', 'convexity']

    # Load shape files as a list of numpy arrays of per-vertex shape values:
    shape_files = [area_file, depth_file, mean_curvature_file,
                   gauss_curvature_file, max_curvature_file,
                   min_curvature_file, thickness_file, convexity_file]
    shape_arrays = []
    column_names = []
    normalize_by_area = False
    for ishape, shape_file in enumerate(shape_files):
        if os.path.exists(shape_file):
            scalars_array, name = read_scalars(shape_file, True, True)
            if scalars_array.size:
                shape_arrays.append(scalars_array)
                column_names.append(shape_names[ishape])

                # Store area array:
                if ishape == 0:
                    normalize_by_area = True
                    area_array = scalars_array.copy()

    # Initialize table file names:
    fundus_table = None
    sulcus_table = None
    norm_fundus_table = None
    norm_sulcus_table = None

    # Loop through features / tables:
    for itable, feature_list in enumerate(feature_lists):

        table_column_names = column_names[:]

        # For each feature, construct a table of average shape values:
        table_file = os.path.join(os.getcwd(), table_names[itable])
        if normalize_by_area:
            norm_table_file = os.path.join(os.getcwd(),
                                           'norm_' + table_names[itable])
        if feature_list:

            # Loop through shape measures:
            columns = []
            norm_columns = []
            for shape_array in shape_arrays:

                # Compute mean shape value per feature:
                mean_values, label_list, surface_areas, \
                norm_mean_values = mean_value_per_label(shape_array,
                    feature_list, exclude_labels, normalize_by_area, area_array)

                # Append mean shape value per feature to columns:
                columns.append(mean_values)
                if normalize_by_area:
                    norm_columns.append(norm_mean_values)

            # Include spectra:
            if itable in [0,1]:
                spectra = spectra_lists[itable]
                spectra_name = spectra_names[itable]
                spectra_IDs = spectra_ID_lists[itable]
                if normalize_by_area:
                    spectra_norm = spectra_norm_lists[itable]

                # Order spectra and convert to comma-delimited strings:
                spectrum_strings = []
                if normalize_by_area:
                    spectrum_norm_strings = []
                for label in label_list:
                    if label in spectra_IDs:
                        spectrum = spectra[spectra_IDs.index(label)]
                        spectrum_string = ','.join([str(x) for x in spectrum])
                        spectrum_strings.append('"' + spectrum_string + '"')
                        if normalize_by_area:
                            spectrum_norm = spectra_norm[spectra_IDs.index(label)]
                            spectrum_norm_string = ','.join([str(x) for x in spectrum_norm])
                            spectrum_norm_strings.append('"' + spectrum_norm_string + '"')
                    else:
                        spectrum_strings.append('')
                        spectrum_norm_strings.append('')

                # Append spectral shape name and values to relevant columns:
                columns.append(spectrum_strings)
                table_column_names.append(spectra_name)
                if normalize_by_area:
                    norm_columns.append(spectrum_norm_strings)

            # Write labels to table:
            write_columns(label_list, 'label', table_file, delimiter)
            if normalize_by_area:
                write_columns(label_list, 'label', norm_table_file, delimiter)

            # Append columns of shape values to table:
            if columns:
                write_columns(columns, table_column_names, table_file,
                              delimiter, table_file)
                if normalize_by_area:
                    write_columns(norm_columns, table_column_names,
                                  norm_table_file, delimiter,
                                  norm_table_file)
        else:
            # Write something to table:
            write_columns([], '', table_file, delimiter)
            if normalize_by_area:
                write_columns([], '', norm_table_file, delimiter)

        # Return correct table file name:
        if itable == 0:
            label_table = table_file
        elif itable == 1:
            sulcus_table = table_file
        elif itable == 2:
            fundus_table = table_file
        if normalize_by_area:
            if itable == 0:
                norm_label_table = norm_table_file
            elif itable == 1:
                norm_sulcus_table = norm_table_file
            elif itable == 2:
                norm_fundus_table = norm_table_file

    return label_table, sulcus_table, fundus_table, \
           norm_label_table, norm_sulcus_table, norm_fundus_table


def write_vertex_shapes_table(table_file,
                              labels_or_file, sulci=[], fundi=[],
                              area_file='', depth_file='', depth_rescaled_file='',
                              mean_curvature_file='', gauss_curvature_file='',
                              max_curvature_file='', min_curvature_file='',
                              thickness_file='', convexity_file='',
                              delimiter=','):
    """
    Make a table of shape values per vertex.

    Parameters
    ----------
    table_file : output filename (without path)
    labels_or_file : list or string
        label number for each vertex or name of VTK file with index scalars
    sulci :  list of integers
        indices to sulci, one per vertex, with -1 indicating no sulcus
    fundi :  list of integers
        indices to fundi, one per vertex, with -1 indicating no fundus
    area_file :  string
        name of VTK file with scalar surface area values
    depth_file :  string
        name of VTK file with scalar depth values
    depth_rescaled_file :  string
        name of VTK file with scalar rescaled depth values
    mean_curvature_file :  string
        name of VTK file with scalar mean curvature values
    gauss_curvature_file :  string
        name of VTK file with scalar Gaussian curvature values
    max_curvature_file :  string
        name of VTK file with scalar maximum curvature values
    min_curvature_file :  string
        name of VTK file with scalar minimum curvature values
    thickness_file :  string
        name of VTK file with scalar thickness values
    convexity_file :  string
        name of VTK file with scalar convexity values
    delimiter : string
        delimiter between columns, such as ','

    Returns
    -------
    shape_table : table file name for vertex shape values

    Examples
    --------
    >>> import os
    >>> from mindboggle.utils.io_vtk import read_scalars
    >>> from mindboggle.shapes.tabulate import write_vertex_shapes_table
    >>> #
    >>> table_file = 'vertex_shapes.csv'
    >>> path = os.environ['MINDBOGGLE_DATA']
    >>> labels_or_file = os.path.join(path, 'arno', 'labels', 'lh.labels.DKT25.manual.vtk')
    >>> sulci_file = os.path.join(path, 'arno', 'features', 'sulci.vtk')
    >>> fundi_file = os.path.join(path, 'arno', 'features', 'fundi.vtk')
    >>> sulci, name = read_scalars(sulci_file)
    >>> fundi, name = read_scalars(fundi_file)
    >>> area_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.area.vtk')
    >>> depth_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.depth.vtk')
    >>> depth_rescaled_file = os.path.join(path, 'arno', 'shapes', 'depth_rescaled.vtk')
    >>> mean_curvature_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.curv.avg.vtk')
    >>> gauss_curvature_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.curv.gauss.vtk')
    >>> max_curvature_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.curv.max.vtk')
    >>> min_curvature_file = os.path.join(path, 'arno', 'shapes', 'lh.pial.curv.min.vtk')
    >>> thickness_file = ''
    >>> convexity_file = ''
    >>> delimiter = ','
    >>> #
    >>> write_vertex_shapes_table(table_file, labels_or_file, sulci, fundi, \
    >>>     area_file, depth_file, depth_rescaled_file, mean_curvature_file, \
    >>>     gauss_curvature_file, max_curvature_file, min_curvature_file, \
    >>>     thickness_file, convexity_file, delimiter)

    """
    import os
    import numpy as np
    from mindboggle.utils.io_vtk import read_scalars
    from mindboggle.utils.io_file import write_columns

    # Make sure inputs are lists:
    if isinstance(labels_or_file, np.ndarray):
        labels = labels_or_file.tolist()
    elif isinstance(labels_or_file, list):
        labels = labels_or_file
    elif isinstance(labels_or_file, str):
        labels, name = read_scalars(labels_or_file)
    if isinstance(sulci, np.ndarray):
        sulci = sulci.tolist()
    if isinstance(fundi, np.ndarray):
        fundi = fundi.tolist()

    # Feature names and corresponding feature lists:
    feature_names = ['label', 'sulcus', 'fundus']
    feature_lists = [labels, sulci, fundi]

    # Shape names and corresponding shape files:
    shape_names = ['area', 'depth', 'depth_rescaled', 'mean_curvature',
                   'gauss_curvature', 'max_curvature', 'min_curvature',
                   'thickness', 'convexity']
    shape_files = [area_file, depth_file, depth_rescaled_file,
                   mean_curvature_file, gauss_curvature_file,
                   max_curvature_file, min_curvature_file,
                   thickness_file, convexity_file]

    # Append columns of per-vertex scalar values:
    columns = []
    column_names = []
    for ifeature, values in enumerate(feature_lists):
        if values:
            if not columns:
                indices = range(len(values))
            columns.append(values)
            column_names.append(feature_names[ifeature])

    for ishape, shape_file in enumerate(shape_files):
        if os.path.exists(shape_file):
            scalars, name = read_scalars(shape_file)
            if len(scalars):
                if not columns:
                    indices = range(len(scalars))
                columns.append(scalars)
                column_names.append(shape_names[ishape])

    # Prepend with column of indices and write table
    shapes_table = os.path.join(os.getcwd(), table_file)
    write_columns(indices, 'index', shapes_table, delimiter)
    write_columns(columns, column_names, shapes_table, delimiter, shapes_table)

    return shapes_table

