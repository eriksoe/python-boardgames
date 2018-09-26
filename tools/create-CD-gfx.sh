#!/bin/bash

function doColor() {
    colorName="$1"
    ringColor="$2"
    bgColor="$3"
    symbolColor="$4"

    cat <<EOF | magick-script -

-size 48x48 xc:Transparent
-background transparent

-draw "fill white Circle 24,24 24,4"

# Clip sector
( xc:Transparent -draw "fill white Polygon 24,0 100,0 124,82 24,24" -layers merge ) -compose dstIn -composite

# Add shadow
( +clone -brightness-contrast 0x-30 -blur 0x1.2 -normalize -shade 120x60 -gamma 2.5  ) -compose Atop -composite

# Tint - with Player color ring
( xc:transparent -draw "fill #ff5555 Rectangle 0,0 48,48 fill transparent stroke ${ringColor} Circle 24,24 24,8"
) -compose Multiply -composite

-write boardgame/gfx/CD-red-${colorName}.gif
+delete
#----------
-compose over
-size 48x48 xc:Transparent
-background transparent

-draw "fill white Circle 24,24 24,4"

# Clip sector
( xc:Transparent -draw "fill green Polygon 24,0 -100,0 -76,82 24,24" -layers merge ) -compose dstIn -composite

# Add shadow
( +clone -brightness-contrast 0x-30 -blur 0x1.2 -normalize -shade 120x60 -gamma 2.5  ) -compose Atop -composite

# Tint - with Player color ring
( xc:transparent -draw "fill #9999ff Rectangle 0,0 48,48 fill transparent stroke ${ringColor} Circle 24,24 24,8"
) -compose Multiply -composite
#( xc:transparent -draw "fill #9999ff Rectangle 0,0 48,48" ) -compose Multiply -composite

-write boardgame/gfx/CD-blue-${colorName}.gif
+delete
#----------
-compose over
-size 48x48 xc:Transparent
-background transparent

-draw "fill white Circle 24,24 24,4"

# Clip sector
( xc:Transparent -draw "fill green Polygon 124,82 24,24 -76,82 24,500" -layers merge ) -compose dstIn -composite

# Add shadow
( +clone -brightness-contrast 0x-30 -blur 0x1.2 -normalize -shade 120x60 -gamma 2.5  ) -compose Atop -composite

# Tint - with Player color ring
( xc:transparent -draw "fill #33dd33 Rectangle 0,0 48,48 fill transparent stroke ${ringColor} Circle 24,24 24,8"
) -compose Multiply -composite
#( xc:transparent -draw "fill #55ff55 Rectangle 0,0 48,48" ) -compose Multiply -composite

-write boardgame/gfx/CD-green-${colorName}.gif
+delete

#----------
-compose over
-size 48x48 xc:Transparent
-background transparent

-draw "fill white Circle 24,24 24,14"

# Add shadow
( #+clone
xc:Transparent
-draw "fill white Circle 24,24 24,19"
-brightness-contrast 0x-30 -blur 0x3 -normalize -shade 120x60 -write foo.png -gamma 1.5  ) -compose Atop -composite

# Tint - with Player color and symbol
( xc:transparent -draw "
  fill ${bgColor} Rectangle 0,0 48,48"
#  fill transparent stroke #ddd Circle 24,24 24,17"
-draw "fill ${symbolColor}
Rectangle 23.5,19 24.5,29
Rectangle 19,23.5 29,24.5"
) -compose Multiply -composite

-write boardgame/gfx/CD-king-${colorName}.gif
+delete

#---------- Test composing pieces:
-compose over
boardgame/gfx/CD-red-${colorName}.gif
boardgame/gfx/CD-blue-${colorName}.gif
boardgame/gfx/CD-green-${colorName}.gif
boardgame/gfx/CD-king-${colorName}.gif
-flatten
-write all-${colorName}.gif
+delete
EOF
}

doColor W white "#fff" "#bbb"
doColor B "#555" "#555" "#eee"

