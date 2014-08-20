#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from  glumpy import app
from glumpy.graphics.collection import LineCollection


vertex = """
// Those are added automatically by the collection
// -----------------------------------------------
// uniform   sampler2D uniforms;
// uniform   vec3      uniforms_shape;
// attribute float     collection_index;
//
// attribute vec3 position;
// attribute vec4 color;
// ... user-defined through collection init dtypes
// -----------------------------------------------

uniform float rows, cols;
varying vec4 v_color;
void main()
{
    // This line is mandatory and is responsible for fetching uniforms
    // from the underlying uniform texture
    fetch_uniforms();

    // color can end up being an attribute or a varying
    // If you want to make sure to pass it to the fragment,
    // It's better to define it here explicitly
    if (selected > 0.0)
        v_color = vec4(1,1,1,1);
    else
        v_color = color;

    float index = collection_index;

    // Compute row/col from collection_index
    float col = mod(index,cols) + 0.5;
    float row = floor(index/cols) + 0.5;
    float x = -1.0 + col * (2.0/cols);
    float y = -1.0 + row * (2.0/rows);
    float width = 0.95 / (1.0*cols);
    float height = 0.95 / (1.0*rows) * amplitude;

    gl_Position = vec4(x + width*position.x, y + height*position.y, 0.0, 1.0);
}
"""

fragment = """
// Collection varyings are not propagated to the fragment shader
// -------------------------------------------------------------
varying vec4 v_color;
void main(void)
{
    gl_FragColor = v_color;
}
"""


rows,cols = 16,20
n, p = rows*cols, 1000
lines = LineCollection(dtypes = [("amplitude", np.float32, 1),
                                 ("selected",  np.float32, 1)],
                       scopes = {"amplitude" : "shared",
                                 "selected" : "shared"},
                       vertex=vertex, fragment=fragment )
lines["rows"] = rows
lines["cols"] = cols

lines.append(np.random.uniform(-1,1,(n*p,3)), itemsize=p)
lines["position"][:,0] = np.tile(np.linspace(-1,+1,p),n)
lines["amplitude"][:n] = np.random.uniform(0.25,0.75,n)
lines["color"][:n] = np.random.uniform(0.25,0.75,(n,4))
lines["selected"] = 0.0

window = app.Window(800,600)
@window.event
def on_draw(dt):
    window.clear(), lines.draw()


@window.event
def on_mouse_motion(x,y,dx,dy):

    y = window.height-y

    # Find the index of the plot under mouse
    col = int(x/float(window.width)*cols) % cols
    row = int(y/float(window.height)*rows) % rows
    index = row*cols + col
    lines["selected"] = 0
    lines["selected"][index] = 1

app.run()
