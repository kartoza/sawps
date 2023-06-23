import React, { useRef, useEffect, useState, useCallback } from 'react';
import maplibregl, { IControl } from 'maplibre-gl';
import { MaplibreExportControl, Size, PageOrientation, Format, DPI} from "@watergis/maplibre-gl-export";
import '@watergis/maplibre-gl-export/dist/maplibre-gl-export.css';
import {RootState} from '../../../app/store';
import {useAppDispatch, useAppSelector } from '../../../app/hooks';
import { 
  setMapReady,
  toggleParcelSelectedState,
  setSelectedProperty,
  resetSelectedProperty,
  selectedParcelsOnRenderFinished,
  onMapEventProcessed,
  toggleMapTheme,
  setInitialMapTheme
} from '../../../reducers/MapState';
import ParcelInterface from '../../../models/Parcel';
import { MapSelectionMode, MapTheme } from "../../../models/Map";
import { UploadMode } from "../../../models/Upload";
import './index.scss';
import CustomNavControl from './NavControl';
import {
  checkLayerVisibility,
  renderHighlightParcelLayers,
  removeHighlightParcelLayers,
  findParcelLayer,
  searchParcel,
  searchProperty,
  getSelectParcelLayerNames
} from './MapUtility';
import PropertyInterface from '../../../models/Property';
import CustomExportControl from './CustomExportControl';
import useThemeDetector from '../../../components/ThemeDetector';

const MAP_STYLE_URL = window.location.origin + '/api/map/styles/'
const MAP_SOURCES = ['sanbi', 'properties', 'NGI Aerial Imagery']
const AERIAL_SOURCE_ID = 'NGI Aerial Imagery'

const TIME_QUERY_PARAM_REGEX = /\?t=\d+/

export default function Map() {
  const dispatch = useAppDispatch()
  const contextLayers = useAppSelector((state: RootState) => state.layerFilter.contextLayers)
  const isMapReady = useAppSelector((state: RootState) => state.mapState.isMapReady)
  const selectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)
  const selectedParcels = useAppSelector((state: RootState) => state.mapState.selectedParcels)
  const selectedProperty = useAppSelector((state: RootState) => state.mapState.selectedProperty)
  const uploadMode = useAppSelector((state: RootState) => state.uploadState.uploadMode)
  const mapEvents = useAppSelector((state: RootState) => state.mapState.mapEvents)
  const mapTheme = useAppSelector((state: RootState) => state.mapState.theme)
  const mapContainer = useRef(null)
  const map = useRef(null)
  const mapNavControl = useRef(null)
  const isDarkTheme = useThemeDetector()

  const onMapMouseEnter = () => {
    if (!map.current) return;    
    // Change the cursor style as a UI indicator.
    map.current.getCanvas().style.cursor = 'pointer';
  }

  const onMapMouseLeave = () => {
    if (!map.current) return;
    map.current.getCanvas().style.cursor = '';
  }

  useEffect(() => {
    dispatch(setInitialMapTheme(isDarkTheme ? MapTheme.Dark : MapTheme.Light))
  }, [isDarkTheme])

  useEffect(() => {
    if (!isMapReady) return;
    if (contextLayers.length === 0) return;
    if (!map.current) return;
    const _mapObj: maplibregl.Map = map.current
    const _layers = _mapObj.getStyle().layers
    for (let i=0; i < _layers.length; ++i) {
      let _layer:any = _layers[i]
      // skip any layer that is not from sanbi and property sources
      if (!('source' in _layer) || !MAP_SOURCES.includes(_layer['source'])) continue
      // skip if no source-layer and not NGI aerial imagery
      if (!('source-layer' in _layer) && _layer['source'] !== AERIAL_SOURCE_ID) continue
      // skip if current selection mode is parcel selection and highlighted layer for selecting parcel
      if (selectionMode === MapSelectionMode.Parcel && _layer['id'].includes('-select-parcel')) continue
      let _source_layer = 'source-layer' in _layer ? _layer['source-layer'] : _layer['source']
      const _is_visible = checkLayerVisibility(_source_layer, contextLayers)
      _mapObj.setLayoutProperty(_layer['id'], 'visibility', _is_visible ? 'visible' : 'none')
    }

    let _parcelLayer = findParcelLayer(contextLayers)
    let _selectParcelLayers = getSelectParcelLayerNames(_parcelLayer.layer_names)
    for (let i=0; i < _selectParcelLayers.length; ++i) {
      _mapObj.on('mouseenter', _selectParcelLayers[i], onMapMouseEnter)
      _mapObj.on('mouseleave', _selectParcelLayers[i], onMapMouseLeave)
    }
    return () => {
      for (let i=0; i < _selectParcelLayers.length; ++i) {
        _mapObj.off('mouseenter', _selectParcelLayers[i], onMapMouseEnter)
        _mapObj.off('mouseleave', _selectParcelLayers[i], onMapMouseLeave)
      }
    }
  }, [contextLayers, isMapReady])

  /* Called when selectionMode is changed */
  useEffect(() => {
    if (!isMapReady) return;
    if (contextLayers.length === 0) return;
    if (!map.current) return;
    
    let _mapObj: maplibregl.Map = map.current
    let _parcelLayer = findParcelLayer(contextLayers)
    if (typeof _parcelLayer === 'undefined') return;
    if (selectionMode === MapSelectionMode.Parcel) {
      renderHighlightParcelLayers(_mapObj, _parcelLayer.layer_names)
    } else {
      removeHighlightParcelLayers(_mapObj, _parcelLayer.layer_names)
    }
  }, [selectionMode])

  useEffect(() => {
    if (mapTheme === MapTheme.None) return;
    if (map.current) {
      dispatch(setMapReady(false))
      map.current.setStyle(`${MAP_STYLE_URL}?theme=${mapTheme}`)
      if (mapNavControl.current) {
        mapNavControl.current.updateThemeSwitcherIcon(mapTheme)
      }
    } else {
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: `${MAP_STYLE_URL}?theme=${mapTheme}`,
        minZoom: 5
      })
      // add exporter dialog
      mapNavControl.current = new CustomNavControl({
        showCompass: false,
        showZoom: true
      }, {
        initialTheme: mapTheme,
        onThemeSwitched: () => { dispatch(toggleMapTheme()) }
      })
      map.current.addControl(mapNavControl.current, 'bottom-left')
      map.current.addControl(mapNavControl.current.getExportControl(), 'bottom-left')
      map.current.on('load', () => {
        dispatch(setMapReady(true))
        map.current.on('mouseenter', 'properties', onMapMouseEnter)
        map.current.on('mouseleave', 'properties', onMapMouseLeave)
      })
      map.current.on('styledata', () => {
        dispatch(setMapReady(true))
      })
    }
  }, [mapTheme]);

  /* Callback when map is on click. */
  const mapOnClick = useCallback((e: any) => {
    if (contextLayers.length === 0) return;
    if (selectionMode === MapSelectionMode.None) return;
    let _parcelLayer = findParcelLayer(contextLayers)
    if (typeof _parcelLayer === 'undefined') return;
    if (selectionMode === MapSelectionMode.Parcel) {
      // TODO: perhaps skip search if not in the parcel zoom?
      // find parcel
      searchParcel(e.lngLat, selectedProperty.id, (parcel: ParcelInterface) => {
        if (parcel) {
          dispatch(toggleParcelSelectedState(parcel))
        }
      })
    } else if (selectionMode === MapSelectionMode.Property && uploadMode === UploadMode.None) {
      // TODO: perhaps skip search if not in the properties zoom?
      // find parcel
      searchProperty(e.lngLat, (property: PropertyInterface) => {
        if (property) {
          dispatch(setSelectedProperty(property))
        } else {
          dispatch(resetSelectedProperty())
        }
      })
    }
  }, [contextLayers, selectionMode, uploadMode, selectedProperty])

  useEffect(() => {
    if (!map.current) return;
    map.current.on('click', mapOnClick)
    return () => {
      map.current.off('click', mapOnClick)
    }
  }, [contextLayers, selectionMode, uploadMode, selectedProperty])

  // render selected+unselected parcel
  useEffect(() => {
    let _mapObj: maplibregl.Map = map.current
    let _has_removed = false
    for (let i = 0; i < selectedParcels.length; ++i) {
      let parcel = selectedParcels[i]
      let _feature_id = { source: 'sanbi', sourceLayer: parcel.layer, id: parcel.id }
      let _selected = parcel.isRemoved ? false : true
      _mapObj.setFeatureState(
        _feature_id,
        { 'parcel-selected': _selected }
      )
      if (parcel.isRemoved) {
        _has_removed = true
      }
    }
    if (_has_removed) {
      dispatch(selectedParcelsOnRenderFinished())
    }
  }, [selectedParcels])

  useEffect(() => {
    if (mapEvents.length === 0) return
    let _mapObj: maplibregl.Map = map.current
    for (let i=0; i < mapEvents.length; ++i) {
      let _event = mapEvents[i]
      if (_event.name === 'REFRESH_PROPERTIES_LAYER') {
        // add query param t to properties layer to refresh it
        let _properties_source = _mapObj.getSource('properties') as any;
        let _url = _properties_source['tiles'][0]
        _url = _url.replace(TIME_QUERY_PARAM_REGEX, `?t=${Date.now()}`)
        // Set the tile url to a cache-busting url (to circumvent browser caching behaviour):
        _properties_source.tiles = [ _url ]

        // Remove the tiles for a particular source
        _mapObj.style.sourceCaches['properties'].clearTiles()

        // Load the new tiles for the current viewport (map.transform -> viewport)
        _mapObj.style.sourceCaches['properties'].update(_mapObj.transform)

        // Force a repaint, so that the map will be repainted without you having to touch the map
        _mapObj.triggerRepaint()
      } else if (_event.name === 'PROPERTY_SELECTED' || _event.name === 'BOUNDARY_FILES_UPLOADED') {
        // parse bbox from payload
        if (_event.payload && _event.payload.length === 4) {
          let _bbox = _event.payload.map(Number)
          _mapObj.fitBounds([[_bbox[0], _bbox[1]], [_bbox[2], _bbox[3]]], {
              padding: 100,
              maxZoom: 16
          })
        }
      }
    }
    dispatch(onMapEventProcessed([...mapEvents]))
  }, [mapEvents])

  return (
      <div className="map-wrap">
        <div ref={mapContainer} className="map" />
      </div>
  );
}
