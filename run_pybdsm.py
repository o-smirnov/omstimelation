#!/usr/bin/env python
import sys
from omegaconf import OmegaConf
import bdsf as bdsm

args = OmegaConf.create(sys.argv[1])

# these arguments belong to write_catalog() -- this gives their names -- the rest are used by process_image()
WRITE_CATALOG_ARGS = dict(outfile='outfile', catalog_type='catalog_type', catalog_format='format')

# enforce type conversions
ARG_TYPES = dict(rms_box=tuple)

# form args for process_image
process_image_args = dict(
    print_timing=True,
    quiet=True,
    # for some reason process_image locks up unless this is set to True. Something to do with the progress bar filling up buffers on stdout?
    #verbose_fitting=True,
)
for arg, value in args.items():
    if arg not in WRITE_CATALOG_ARGS and arg != 'image':
        if arg in ARG_TYPES:
            value = ARG_TYPES[arg](value)
        process_image_args[arg] = value

# form args for write_catalog
write_catalog_args = dict(clobber=True)
for arg, value in args.items():
    if arg in WRITE_CATALOG_ARGS:
        if arg in ARG_TYPES:
            value = ARG_TYPES[arg](value)
        write_catalog_args[WRITE_CATALOG_ARGS[arg]] = value


print(f"process_image arguments: {args.image} {process_image_args}")
sys.stdout.flush()
print(f"write_catalog arguments: {write_catalog_args}")
sys.stdout.flush()

print(f"calling process_image")
sys.stdout.flush()
img = bdsm.process_image(args.image, **process_image_args)

print(f"calling write_catalog")
sys.stdout.flush()
img.write_catalog(**write_catalog_args)

print(f"finished")
sys.stdout.flush()
