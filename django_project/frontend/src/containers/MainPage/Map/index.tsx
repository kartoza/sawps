import React, { useRef, useEffect, useState, useCallback } from 'react';
import axios from "axios";
import ReactDOM from "react-dom/client";
import maplibregl, { IControl } from 'maplibre-gl';
import {RootState} from '../../../app/store';
import {useAppDispatch, useAppSelector } from '../../../app/hooks';
import { setMapReady, toggleParcelSelectedState, resetSelectedParcels } from '../../../reducers/MapState';
import ParcelInterface from '../../../models/Parcel';
import { MapSelectionMode } from "../../../models/MapSelectionMode";
import './index.scss';
import CustomNavControl from './NavControl';
import {
  checkLayerVisibility,
  renderHighlightParcelLayers,
  removeHighlightParcelLayers,
  findParcelLayer,
  searchParcel
} from './MapUtility';

const MAP_STYLE_URL = window.location.origin + '/api/map/styles/'

export default function Map() {
  const dispatch = useAppDispatch()
  const contextLayers = useAppSelector((state: RootState) => state.layerFilter.contextLayers)
  const isMapReady = useAppSelector((state: RootState) => state.mapState.isMapReady)
  const selectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)
  const selectedParcels = useAppSelector((state: RootState) => state.mapState.selectedParcels)
  const mapContainer = useRef(null);
  const map = useRef(null);

  useEffect(() => {
    if (!isMapReady) return;
    if (contextLayers.length === 0) return;
    if (!map.current) return;
    const _mapObj: maplibregl.Map = map.current
    const _layers = _mapObj.getStyle().layers
    for (let i=0; i < _layers.length; ++i) {
      let _layer:any = _layers[i]
      if (!('source' in _layer) || !('source-layer' in _layer) || _layer['source'] !== 'sanbi') continue
      if (selectionMode === MapSelectionMode.Parcel && _layer['id'].includes('-select-parcel')) continue
      const _is_visible = checkLayerVisibility(_layer['source-layer'], contextLayers)
      _mapObj.setLayoutProperty(_layer['id'], 'visibility', _is_visible ? 'visible' : 'none')
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
      // need to reset any feature-state that has been set
      for (let i = 0; i < selectedParcels.length; ++i) {
        let _parcel = selectedParcels[i]
        let _feature_id = { source: 'sanbi', sourceLayer: _parcel.layer, id: _parcel.id }
        _mapObj.setFeatureState(
          _feature_id,
          { 'parcel-selected': false }
        );
      }
      dispatch(resetSelectedParcels())
    }
  }, [selectionMode])

  useEffect(() => {
      if (map.current) return; //stops map from intializing more than once
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: `${MAP_STYLE_URL}`,
        center: [27.763781680455708, -26.71998940486352], // debug
        zoom: 17,
        minZoom: 5
      })
      map.current.addControl(new CustomNavControl({
        showCompass: true,
        showZoom: true
      }), 'bottom-left')
      map.current.on('load', () => {
        dispatch(setMapReady(true))
      })

  });

  /* Callback when map is on click. */
  const mapOnClick = useCallback((e: any) => {
    if (contextLayers.length === 0) return;
    if (selectionMode === MapSelectionMode.None) return;
    let _parcelLayer = findParcelLayer(contextLayers)
    if (typeof _parcelLayer === 'undefined') return;
    let _mapObj: maplibregl.Map = map.current
    if (selectionMode === MapSelectionMode.Parcel) {
      // find parcel
      searchParcel(e.lngLat, (parcel: ParcelInterface) => {
        if (parcel) {
          // toggle selection
          let _feature_id = { source: 'sanbi', sourceLayer: parcel.layer, id: parcel.id }
          let _selected = _mapObj.getFeatureState(_feature_id)
          if (_selected) {
            _selected = _selected['parcel-selected']
          }
          _mapObj.setFeatureState(
            _feature_id,
            { 'parcel-selected': !_selected }
          );
          dispatch(toggleParcelSelectedState(parcel))
        }
      })
    }
  }, [contextLayers, selectionMode])

  useEffect(() => {
    map.current.on('click', mapOnClick)
    return () => {
      map.current.off('click', mapOnClick)
    }
  }, [contextLayers, selectionMode])

  return (
      <div className="map-wrap">
        <div ref={mapContainer} className="map" />
      </div>
  );
}
