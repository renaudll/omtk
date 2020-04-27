Compounds are isolate dg nodes networks encapsulated in a maya file.
They can be re-used manually or with omtk-compound.

# omtk.Follicle

A surface follicle network with only DG nodes

## Inputs:
* _nurbsSurface_ surface: The surface to follow
* _float_ parameterU: The U coordinate to follow
* _float_ parameterV: The V coordinate to follow

## Outputs:
* _matrix_ output: The follicle transform.

# omtk.InfinityFollicle

A surface follicle that can continue linearly out of the surface bounds

## Inputs:
* _nurbsSurface_ surface: The surface to follow
* _float_ parameterU: The U coordinate to follow
* _float_ parameterV: The V coordinate to follow

## Outputs:
* _matrix_ output: The follicle transform

# omtk.TwistExtractor

Extract start and end roll for the middle object in a chain of 3.

## Inputs
* _matrix_ bind1: The (static) original transform for the first object
* _matrix_ bind2: The (static) original transform for the middle object
* _matrix_ bind3: The (static) original transform for the last object
* _matrix_ inn1: The current transform for the first object
* _matrix_ inn2: The current transform for the middle object
* _matrix_ inn3: The current transform for the last object

## Outputs
* _float_ outTwistS: The extracted twist between the first and middle object.
* _float_ outTwistE: The extracted twist between the middle and last object.
