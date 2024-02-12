import axios from "axios";
import ContextLayerInterface from '../../../models/ContextLayer';
import ParcelInterface from '../../../models/Parcel';
import PropertyInterface from "../../../models/Property";
import { MapTheme, PopulationCountLegend } from "../../../models/Map";
import { GeoJSONSource } from "maplibre-gl";

const SEARCH_PARCEL_URL = '/api/map/search/parcel/'
const SEARCH_PROPERTY_URL = '/api/map/search/property/'
const BOUNDARY_FILE_GEOJSON_URL = '/api/upload/boundary-file/'
export const MIN_SELECT_PARCEL_ZOOM_LEVEL = 9
export const MIN_SELECT_PROPERTY_ZOOM_LEVEL = 9
export const MIN_SEARCH_PARCEL_ZOOM_LEVEL = 9 // search erf, farm_portion, holding and display the info on popup
const PARCELS_ORIGINAL_ZOOM_LEVELS: any = {
    'erf': 14,
    'holding': 12,
    'farm_portion': 12,
    'parent_farm': 9
}
export const MIN_PROVINCE_ZOOM_LEVEL = 5
export const MAX_PROVINCE_ZOOM_LEVEL = 8

/**
 * Determine layer visibility based on selected context layers
 * @param source_layer
 * @param contextLayers
 * @returns
 */
export const checkLayerVisibility = (source_layer: string, contextLayers: ContextLayerInterface[]): boolean => {
    const contextLayer = contextLayers.find(element => element.layer_names && element.layer_names.includes(source_layer))
    if (contextLayer) {
      return contextLayer.isSelected
    }
    return true
}

/**
 * Return all layers for select parcels
 * @param layer_names
 * @returns
 */
export const getSelectParcelLayerNames = (layer_names: string[]) => {
    let _results: string[] = []
    for (let _idx = 0; _idx < layer_names.length; ++_idx) {
        let _layer_name = `${layer_names[_idx]}-select-parcel`
        _results.push(_layer_name)
    }
    return _results
}

/**
 * Render parcel layers for selection
 * @param map
 * @param layer_names
 */
export const renderHighlightParcelLayers = (map: maplibregl.Map, layer_names: string[]) => {
    for (let _idx = 0; _idx < layer_names.length; ++_idx) {
        if (layer_names[_idx].indexOf('_labels') > -1) continue
        // parent_farm will not be in select mode because it is broken down to smaller parcels (farm_portions)
        // if (layer_names[_idx].indexOf('parent_farm') > -1) continue
        let _layer_name = `${layer_names[_idx]}-select-parcel`
        if (typeof map.getLayer(_layer_name) === 'undefined') {
            map.addLayer({
                'id': _layer_name,
                'type': 'fill',
                'source': 'sanbi',
                'source-layer': `${layer_names[_idx]}`,
                'minzoom': PARCELS_ORIGINAL_ZOOM_LEVELS[layer_names[_idx]],
                'layout': {},
                'paint': {
                'fill-color': '#F9A95D',
                'fill-opacity': 0.4
                }
            }, 'erf');
        }
        if (typeof map.getLayer(`${_layer_name}-line`) === 'undefined') {
            // add line color
            map.addLayer({
                'id': `${_layer_name}-line`,
                'type': 'line',
                'source': 'sanbi',
                'source-layer': `${layer_names[_idx]}`,
                'layout': {},
                'paint': {
                'line-color': '#FF0000',
                'line-width': [
                    'case',
                    ['boolean', ['feature-state', 'parcel-selected'], false], 4,
                    0
                ]
                }
            }, `${layer_names[_idx]}-highlighted`);
        }
    }
}

/**
 * Remove parcel layers when exits parcel selection mode
 * @param map
 * @param layer_names
 */
export const removeHighlightParcelLayers = (map: maplibregl.Map, layer_names: string[]) => {
    for (let _idx = 0; _idx < layer_names.length; ++_idx) {
        let _layer_name = `${layer_names[_idx]}-select-parcel`
        let _layer = map.getLayer(_layer_name)
        if (typeof _layer !== 'undefined') {
            map.removeLayer(_layer_name)
        }
        _layer = map.getLayer(`${_layer_name}-line`)
        if (typeof _layer !== 'undefined') {
            map.removeLayer(`${_layer_name}-line`)
        }
    }
}

/**
 * Find context layer from Cadastral boundaries: erf, farm_portion, holding, and parent_farm
 * @param contextLayers
 * @returns
 */
export const findParcelLayer = (contextLayers: ContextLayerInterface[]): ContextLayerInterface => {
    return contextLayers.find((element) => element.name.toLowerCase() === 'cadastral boundaries')
}

/**
 * Find context layer from Biodiversity, Ecosystems, Protected Areas
 * @param contextLayers
 * @returns
 */
export const findAreaLayers = (contextLayers: ContextLayerInterface[]): string[] => {
    const areaLayers = ['biome type', 'critical biodiversity areas', 'protected areas']
    let _layers = contextLayers.reduce((acc, element) => {
        if (element.isSelected && areaLayers.includes(element.name.toLowerCase())) {
            acc.push(...element.layer_names)
        }
        return acc;
    }, [])
    return _layers
}

/**
 * Find context layer from Properties
 * @param contextLayers
 * @returns
 */
export const findPropertiesLayer = (contextLayers: ContextLayerInterface[]): ContextLayerInterface => {
    return contextLayers.find((element) => element.name.toLowerCase() === 'properties')
}


/**
 * Check if context layer is selected
 * @param contextLayers
 * @returns
 */
export const isContextLayerSelected = (contextLayers: ContextLayerInterface[], contextLayerName: string): boolean => {
    let _layer = contextLayers.find((element) => element.name.toLowerCase() === contextLayerName)
    if (_layer) {
        return _layer.isSelected
    }
    return false
}


/**
 * Search parcel by coordinate
 * Note: LngLat is in srid 4326
 * @param lngLat
 * @param callback
 */
export const searchParcel = (lngLat: maplibregl.LngLat, propertyId: number, currentZoom: number, callback: (parcel: ParcelInterface) => void) => {
    axios.get(SEARCH_PARCEL_URL + `?lat=${lngLat.lat}&lng=${lngLat.lng}&property_id=${propertyId}&zoom=${currentZoom}`).then((response) => {
        if (response.data) {
            callback(response.data as ParcelInterface)
        } else {
            callback(null)
        }
    }).catch((error) => {
        if (error.response && error.response.status === 404) {
            // perhaps there is other way to stop axios printing 404 to log?
            console.clear()
        }
        callback(null)
    })
}

/**
 * Add layer to map
 * @param layerId
 * @param mapObj
 * @param layerObj
 * @param beforeLayerId
 * @returns true if layer does not exist
 */
export const addLayerToMap = (layerId: string, mapObj: maplibregl.Map, layerObj: any, beforeLayerId?: string): boolean => {
    if (!mapObj) return false
    if (typeof mapObj.getLayer(layerId) === 'undefined') {
        mapObj.addLayer(layerObj, beforeLayerId)
        return true
    }
    return false
}

/**
 * Remove layer from map if exists
 * @param layerId name of the layer
 * @param mapObj map reference object
 */
export const removeLayerFromMap = (layerId: string, mapObj: maplibregl.Map) => {
    if (!mapObj) return;
    let _layer = mapObj.getLayer(layerId)
    if (typeof _layer !== 'undefined') {
        mapObj.removeLayer(layerId)
    }
}

/**
 * Search property by coordinate
 * Note: LngLat is in srid 4326
 * @param lngLat
 * @param callback
 */
export const searchProperty = (lngLat: maplibregl.LngLat, callback: (parcel: PropertyInterface) => void) => {
    axios.get(SEARCH_PROPERTY_URL + `?lat=${lngLat.lat}&lng=${lngLat.lng}`).then((response) => {
        if (response.data) {
            callback(response.data as PropertyInterface)
        } else {
            callback(null)
        }
    }).catch((error) => {
        if (error.response && error.response.status === 404) {
            // perhaps there is other way to stop axios printing 404 to log?
            console.clear()
        }
        callback(null)
    })
}

// Mapping of LayerName with FeatureName to be queried and display in the popup
const FEATURE_NAME_MAPPING:{ [id: string] : string; } = {
    'ecosystems': 'name_18',
    'biodiversity': 'sensfeat',
    'protected': 'site_type',
    'erf': 'cname',
    'farm_portion': 'cname',
    'holding': 'cname',
    'parent_farm': 'cname'
}

// Mapping of LayerName with its Label to displayed in the popup
const GROUP_NAME_MAPPING:{ [id: string] : string; } = {
    'ecosystems': 'Ecosystem Type',
    'biodiversity': 'Critical Biodiversity Area',
    'protected': 'Protected Area',
    'erf': 'Erf Cname',
    'farm_portion': 'Farm Portion Cname',
    'holding': 'Holding Cname',
    'parent_farm': 'Parent Farm Cname'
}

/**
 * Get value from feature based on sourceLayer
 * @param feature GeoJson Object
 * @returns
 */
const getPropertyOfFeature = (feature: any):[string, string] => {
    let _feature_key = null
    let _feature_map_key = null
    for (let _map_key in FEATURE_NAME_MAPPING) {
        if (feature['sourceLayer'].includes(_map_key)) {
            _feature_map_key = _map_key
            _feature_key = FEATURE_NAME_MAPPING[_map_key]
            break;
        }
    }
    if (_feature_key === null) return [null, null]
    if ('properties' in feature && _feature_key in feature['properties']) {
        return [_feature_map_key, feature['properties'][_feature_key]]
    }
    return [null, null]
}

const concatFeatureValues = (feature_map_key: string, featureValues: string[]): string => {
    if (featureValues.length === 2)
        return `${GROUP_NAME_MAPPING[feature_map_key]}: ${featureValues[0]} and ${featureValues[1]}`
    return `${GROUP_NAME_MAPPING[feature_map_key]}: ${featureValues.join(', ')}`
}

export const getMapPopupDescription = (features: Object[]):string => {
    // group by source-layer
    let _groups:{ [id: string] : string[]; } = {}
    for (let i=0; i < features.length; ++i) {
        let _feature:any = features[i]
        let [_featureMapKey, _featureValue] = getPropertyOfFeature(_feature)
        if (_featureValue) {
            if (_featureMapKey in _groups) {
                if (!_groups[_featureMapKey].includes(_featureValue)) {
                    _groups[_featureMapKey].push(_featureValue)
                }
            } else {
                _groups[_featureMapKey] = [_featureValue]
            }
        }
    }
    let _htmlResult = ''
    let _groupsLength = Object.keys(_groups).length
    if (_groupsLength === 0) return _htmlResult
    if (_groupsLength === 1) {
        let _group = Object.keys(_groups)[0]
        _htmlResult += concatFeatureValues(_group, _groups[_group])
    } else {
        let _idx = 0
        for (let _group in _groups) {
            let _featureValues = concatFeatureValues(_group, _groups[_group])
            _htmlResult += `${_featureValues}`
            if (_idx < _groupsLength - 1) {
                _htmlResult += '<hr/>'
            }
            _idx++
        }
    }
    return _htmlResult
}

/**
 * Add invisible fill layers for parcels to handle on click inside the layer
 * @param mapObj
 */
export const addParcelInvisibleFillLayers = (mapObj: maplibregl.Map) => {
    addLayerToMap('erf-invisible-fill', mapObj, {
        'id': 'erf-invisible-fill',
        'type': 'fill',
        'source': 'sanbi',
        'source-layer': 'erf',
        'minzoom': 14,
        'layout': {'visibility': 'visible'},
        'paint': {
            'fill-color': 'rgba(255, 255, 255, 0)',
            'fill-opacity': 0
        }
    }, 'erf')
    addLayerToMap('holding-invisible-fill', mapObj, {
        'id': 'holding-invisible-fill',
        'type': 'fill',
        'source': 'sanbi',
        'source-layer': 'holding',
        'minzoom': 12,
        'layout': {'visibility': 'visible'},
        'paint': {
            'fill-color': 'rgba(255, 255, 255, 0)',
            'fill-opacity': 0
        }
    }, 'erf')
    addLayerToMap('farm_portion-invisible-fill', mapObj, {
        'id': 'farm_portion-invisible-fill',
        'type': 'fill',
        'source': 'sanbi',
        'source-layer': 'farm_portion',
        'minzoom': 12,
        'layout': {'visibility': 'visible'},
        'paint': {
            'fill-color': 'rgba(255, 255, 255, 0)',
            'fill-opacity': 0
        }
    }, 'erf')
    addLayerToMap('parent_farm-invisible-fill', mapObj, {
        'id': 'parent_farm-invisible-fill',
        'type': 'fill',
        'source': 'sanbi',
        'source-layer': 'parent_farm',
        'minzoom': 9,
        'maxzoom': 11,
        'layout': {'visibility': 'visible'},
        'paint': {
            'fill-color': 'rgba(255, 255, 255, 0)',
            'fill-opacity': 0
        }
    }, 'erf')
}

/**
 * Generate stop for choropleth layer's fill-color
 * @param legends list of break/stop
 * @returns 
 */
const getMapPopulationStops = (legends: PopulationCountLegend[]) => {
    let _stops: any = []
    for (let i=0; i<legends.length; ++i) {
        let _stop = [
            {
                "zoom": 5,
                "value": legends[i].value
            },
            `${legends[i].color}`
        ]
        _stops.push(_stop)
    }
    return _stops
}

/**
 * Add properties/province layers.
 * Available layers:
 *   - properties
 *   - properties-points
 *   - province-count
 *   - properties-label
 * 
 * @param showPopulationCount True if species filter is applied
 * @param mapObj 
 * @param propertiesCount 
 * @param provinceCount 
 */
export const drawPropertiesLayer = (showPopulationCount: boolean, mapObj: maplibregl.Map, currentTheme: MapTheme, shouldRemoveFirst: boolean, propertiesCount?: PopulationCountLegend[], provinceCount?: PopulationCountLegend[]) => {
    if (shouldRemoveFirst) {
        removePropertiesLayer(mapObj)
    }
    if (!showPopulationCount) {
        addLayerToMap('properties', mapObj, {
            "id": "properties",
            "type": "fill",
            "source": "sanbi-dynamic",
            "source-layer": "properties",
            "minzoom": 9,
            "maxzoom": 24,
            "layout": {"visibility": "visible"},
            "paint": {
                "fill-color": "rgba(255, 82, 82, 1)",
                "fill-opacity": 0.8
            }
        }, 'erf-highlighted')
        addLayerToMap('properties-points', mapObj, {
            "id": "properties-points",
            "type": "circle",
            "source": "sanbi-dynamic",
            "source-layer": "properties-points",
            "layout": {"visibility": "visible"},
            "paint": {
                "circle-color": "rgba(255, 82, 82, 0.8)",
                "circle-stroke-width": 1,
                "circle-stroke-color": "rgb(0, 0, 0)"
            },
            "minzoom": 5,
            "maxzoom": 9
        }, 'erf-highlighted')
    } else {
        // add province layer
        if (provinceCount && provinceCount.length > 0) {
            let _provinceLayer = {
                "id": "province-count",
                "type": "fill",
                "source": "sanbi-dynamic",
                "minzoom": 5,
                "maxzoom": 8,
                "layout": {"visibility": "visible"},
                "paint": {
                  "fill-opacity": 1,
                  "fill-color": {
                    "property": "count",
                    "type": "interval",
                    "stops": getMapPopulationStops(provinceCount),
                    "base": 1,
                    "default": "rgba(255, 255, 255, 1)"
                  },
                  "fill-outline-color": "rgba(0, 0, 0, 1)"
                },
                "Z": 0,
                "filter": ["all"],
                "source-layer": "province_population"
            }
            addLayerToMap('province-count', mapObj, _provinceLayer, 'NGI aerial imagery')
        }
        if (propertiesCount && propertiesCount.length > 0) {
            let _propertiesLayer = {
                "id": "properties",
                "type": "fill",
                "source": "sanbi-dynamic",
                "minzoom": 9,
                "maxzoom": 24,
                "layout": {"visibility": "visible"},
                "paint": {
                  "fill-opacity": 1,
                  "fill-color": {
                    "property": "count",
                    "type": "interval",
                    "stops": getMapPopulationStops(propertiesCount),
                    "base": 1,
                    "default": "rgba(255, 0, 255, 1)"
                  },
                  "fill-outline-color": "rgba(0, 0, 0, 1)"
                },
                "Z": 0,
                "filter": ["all"],
                "source-layer": "properties"
            }
            let _propertiesPointsLayer = {
                "id": "properties-points",
                "type": "circle",
                "source": "sanbi-dynamic",
                "source-layer": "properties-points",
                "layout": {"visibility": "visible"},
                "paint": {
                    "circle-color": {
                        "property": "count",
                        "type": "exponential",
                        "stops": getMapPopulationStops(propertiesCount),
                        "base": 1,
                        "default": "rgba(248, 0, 255, 1)"
                    },
                    "circle-stroke-width": 1,
                    "circle-stroke-color": "rgb(0, 0, 0)"
                },
                "minzoom": 5,
                "maxzoom": 9
            }
            addLayerToMap('properties', mapObj, _propertiesLayer, 'erf-highlighted')
            addLayerToMap('properties-points', mapObj, _propertiesPointsLayer, 'erf-highlighted')
        }
    }
    // add label based on maptheme
    let _propertiesLabel = {}
    if (currentTheme === MapTheme.Dark) {
        _propertiesLabel = {
            "id": "properties-label",
            "type": "symbol",
            "source": "sanbi-dynamic",
            "source-layer": "properties-points",
            "minzoom": 7,
            "maxzoom": 24,
            "layout": {
              "text-field": "{name}",
              "text-font": ["Open Sans Bold"],
              "text-size": 12,
              "text-letter-spacing": 0.05,
              "text-offset": [
                'interpolate',
                ['linear'],
                ['zoom'],
                7, ["literal", [0, -1]],
                10, ["literal", [0, -0.75]],
              ]
            },
            "paint": {
              "text-halo-color": "rgba(0, 0, 0, 1)",
              "text-color": "rgba(240, 240, 240, 1)",
              "text-halo-width": 1
            }
        }
    } else {
        _propertiesLabel = {
            "id": "properties-label",
            "type": "symbol",
            "source": "sanbi-dynamic",
            "source-layer": "properties-points",
            "minzoom": 7,
            "maxzoom": 24,
            "layout": {
              "text-field": "{name}",
              "text-font": ["Open Sans Bold"],
              "text-size": 12,
              "text-letter-spacing": 0.05,
              "text-offset": [
                'interpolate',
                ['linear'],
                ['zoom'],
                7, ["literal", [0, -1]],
                10, ["literal", [0, -0.75]],
              ]
            },
            "paint": {
              "text-halo-color": "rgba(191, 191, 191, 1)",
              "text-color": "rgba(35, 35, 35, 1)",
              "text-halo-width": 0.5
            }
          }
    }
    addLayerToMap('properties-label', mapObj, _propertiesLabel, 'erf-highlighted')
}

/**
 * Remove layers related to properties
 * @param mapObj 
 */
export const removePropertiesLayer = (mapObj: maplibregl.Map) => {
    // remove existing layer if any
    removeLayerFromMap('properties', mapObj)
    removeLayerFromMap('province-count', mapObj)
    removeLayerFromMap('properties-points', mapObj)
    removeLayerFromMap('properties-label', mapObj)
    removeLayerFromMap('province-extrude', mapObj)
    removeLayerFromMap('properties-extrude', mapObj)
}

/**
 * Add 3d extrude layer for province population.
 * 
 * @param mapObj 
 * @param provinceCount 
 * @returns 
 */
const addProvinceExtrudeLayer = (mapObj: maplibregl.Map, provinceCount?: PopulationCountLegend[]) => {
    if (!provinceCount || provinceCount.length === 0) return;
    // TODO: Determine max height of province extrude 3d layer
    const PROVINCE_MAX_HEIGHT = 75000
    let _maxValue = Math.max(...provinceCount.map(o => o.value))
    let _provinceExtrudeLayer = {
        "id": "province-extrude",
        "type": "fill-extrusion",
        "source": "sanbi-dynamic",
        "source-layer": "province_population",
        "paint": {
            "fill-extrusion-color": {
                "property": "count",
                "type": "interval",
                "stops": getMapPopulationStops(provinceCount),
                "base": 1,
                "default": "rgba(0, 0, 0, 0)"
            },
            "fill-extrusion-opacity": 1,
            "fill-extrusion-height": ["*", ["/", ['get', 'count'], _maxValue], PROVINCE_MAX_HEIGHT],
            "fill-extrusion-base": 0
        },
        "minzoom": 5,
        "maxzoom": 8
    }
    addLayerToMap('province-extrude', mapObj, _provinceExtrudeLayer, 'provinces_small_scale')
}

/**
 * Add 3d extrude layer for properties population.
 * @param mapObj 
 * @param propertiesCount 
 * @returns 
 */
const addPropertiesExtrudeLayer = (mapObj: maplibregl.Map, propertiesCount?: PopulationCountLegend[]) => {
    if (!propertiesCount || propertiesCount.length === 0) return;
    // TODO: Determine max height of properties extrude 3d layer
    const PROPERTIES_MAX_HEIGHT = 2000
    let _maxValue = Math.max(...propertiesCount.map(o => o.value))
    let _propertiesExtrudeLayer = {
        "id": "properties-extrude",
        "type": "fill-extrusion",
        "source": "sanbi-dynamic",
        "source-layer": "properties",
        "paint": {
            "fill-extrusion-color": {
                "property": "count",
                "type": "interval",
                "stops": getMapPopulationStops(propertiesCount),
                "base": 1,
                "default": "rgba(0, 0, 0, 0)"
            },
            "fill-extrusion-opacity": 1,
            "fill-extrusion-height": ["*", ["/", ['get', 'count'], _maxValue], PROPERTIES_MAX_HEIGHT],
            "fill-extrusion-base": 0
        },
        "minzoom": 9,
        "maxzoom": 24
    }
    addLayerToMap('properties-extrude', mapObj, _propertiesExtrudeLayer, 'properties-label')
}

/**
 * Add 3d layers to the map 
 * @param mapObj 
 * @param provinceCount 
 * @param propertiesCount 
 */
export const showExtrudeLayer = (mapObj: maplibregl.Map, provinceCount?: PopulationCountLegend[], propertiesCount?: PopulationCountLegend[]) => {
    removeExtrudeLayer(mapObj)
    addProvinceExtrudeLayer(mapObj, provinceCount)
    addPropertiesExtrudeLayer(mapObj, propertiesCount)
}

/**
 * Remove 3d layers from the map
 * @param mapObj 
 */
export const removeExtrudeLayer = (mapObj: maplibregl.Map) => {
    removeLayerFromMap('province-extrude', mapObj)
    removeLayerFromMap('properties-extrude', mapObj)
}


/**
 * Draw geojson layer for uploaded shapefile or polygon from drawing tools
 * @param mapObj 
 * @param geojsonData geojson object
 */
const drawGeojsonLayer = (mapObj: maplibregl.Map, geojsonData: any) => {
    let _sourceName = `geojson-upload`
    let _source = mapObj.getSource(_sourceName) as GeoJSONSource
    if (!_source) {
        mapObj.addSource(_sourceName, {
            'type': 'geojson',
            'data': geojsonData
        })
    } else {
        _source.setData(geojsonData)
    }
    let _layer = {
        'id': 'geojson-upload-layer',
        'type': 'line',
        'source': _sourceName,
        'layout': {'visibility': 'visible'},
        "paint": {
            "line-color": '#A31ACB',
            "line-width": 4
        }
    }
    addLayerToMap('geojson-upload-layer', mapObj, _layer, 'erf-highlighted')
}

/**
 * Remove geojson layer from map
 * @param mapObj 
 */
export const removeGeojsonLayer = (mapObj: maplibregl.Map) => {
    removeLayerFromMap('geojson-upload-layer', mapObj)
}

/**
 * Retrieve and draw geojson shapefile or polygon from drawing tools
 * @param mapObj 
 * @param session search boundary session 
 */
export const fetchAndDrawGeojsonLayerFromUpload = (mapObj: maplibregl.Map, session: string) => {
    axios.get(`${BOUNDARY_FILE_GEOJSON_URL}${session}/geojson/`).then((response) => {
        if (response.data && mapObj) {
            drawGeojsonLayer(mapObj, response.data)
        }
    }).catch((error) => {
        console.log('Failed to fetch geojson layer ', error)
    })
}
