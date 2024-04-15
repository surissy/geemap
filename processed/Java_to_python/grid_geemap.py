import ee 
from ee_plugin import Map

#

A sample Earth Engine JavaScript library.
'The script is adapted from https':#code.earthengine.google.com/2bca4e5f36d5a2d642475a98fa421fa9
Credits to Gennadii Donchyts.

#

def generateRasterGrid= function(origin, dx, dy, proj):
    coords = origin.transform(proj).coordinates()
    origin = ee.Image.constant(coords.get(0)).addBands(ee.Image.constant(coords.get(1)))

    pixelCoords = ee.Image.pixelCoordinates(proj)

    grid = pixelCoords \
       .subtract(origin) \
       .divide([dx, dy]).floor() \
       .toInt().reduce(ee.Reducer.sum()).bitwiseAnd(1).rename('grid')

    xy = pixelCoords.reproject(proj.translate(coords.get(0), coords.get(1)).scale(dx, dy))

    id = xy.multiply(ee.Image.constant([1, 1000000])).reduce(ee.Reducer.sum()).rename('id')

    return grid \
      .addBands(id) \
      .addBands(xy)



#**
 # Generates a regular grid using given bounds, specified as geometry.
 #
def generateGrid(xmin, ymin, xmax, ymax, dx, dy, marginx, marginy, opt_proj):
    proj = opt_proj || 'EPSG:4326'

    dx = ee.Number(dx)
    dy = ee.Number(dy)

    xx = ee.List.sequence(xmin, ee.Number(xmax).subtract(ee.Number(dx).multiply(0.1)), dx)
    yy = ee.List.sequence(ymin, ee.Number(ymax).subtract(ee.Number(dy).multiply(0.1)), dy)


def func_sqh(x):
      return yy.map(function(y) {
        x1 = ee.Number(x).subtract(marginx)
        x2 = ee.Number(x).add(ee.Number(dx)).add(marginx)
        y1 = ee.Number(y).subtract(marginy)
        y2 = ee.Number(y).add(ee.Number(dy)).add(marginy)

        coords = ee.List([x1, y1, x2, y2])
        rect = ee.Algorithms.GeometryConstructors.Rectangle(coords, proj, False)

        nx = x1.add(dx.multiply(0.5)).subtract(xmin).divide(dx).floor()
        ny = y1.add(dy.multiply(0.5)).subtract(ymin).divide(dy).floor()

        return ee.Feature(rect) \
          .set({
            'nx': nx.format('%d'),
            'ny': ny.format('%d'),
          })
          # .set({cell_id: x1.format('%.3f').cat('_').cat(y1.format('%.3f')) })
      })

    cells = xx.map(func_sqh
).flatten()



















).flatten()

    return ee.FeatureCollection(cells)
  


def grid_test():

    gridRaster = generateRasterGrid(ee.Geometry.Point(0, 0), 10, 10, ee.Projection('EPSG:4326'))
    m.addLayer(gridRaster.select('id').randomVisualizer(), {}, 'Grid raster', True, 0.5)

    gridVector = generateGrid(-180, -70, 180, 70, 10, 10, 0, 0)
    style = {'fillColor': '00000000'}
    m.addLayer(gridVector.style(**style), {}, 'Grid vector')



exports.generateGrid = generateGrid
exports.generateRasterGrid = generateRasterGrid
exports.grid_test = grid_test
m