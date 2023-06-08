import React, { useRef, useEffect, useState } from 'react';
import ReactDOM from "react-dom/client";
import maplibregl, { IControl } from 'maplibre-gl';
import {RootState} from '../../../app/store';
import {useAppDispatch, useAppSelector } from '../../../app/hooks';
import { setMapReady } from '../../../reducers/MapStatus';
import ContextLayerInterface from '../../../models/ContextLayer';
import './index.scss';

const MAP_STYLE_URL = window.location.origin + '/api/map/styles/'

class CustomNavControl extends maplibregl.NavigationControl {

  _print: HTMLButtonElement;
  _printIcon: HTMLElement;
  _baseMapSelect: HTMLButtonElement;
  _baseMapSelectIcon: HTMLElement;

  constructor(options?: maplibregl.NavigationOptions) {
    // note: this can work for es6 target in tsconfig.json
    super(options);

    // add print icon
    this._print = this._createButton('maplibregl-ctrl-print', (e) => {
      // not implemented yet
    });
    this._printIcon = this._create_element('span', 'maplibregl-ctrl-icon', this._print);
    this._printIcon.setAttribute('aria-hidden', 'true');

    
    // add change base map icon
    this._baseMapSelect = this._createButton('maplibregl-ctrl-base-map-select', (e) => {
      // not implemented yet
    });
    this._baseMapSelectIcon = this._create_element('span', 'maplibregl-ctrl-icon', this._baseMapSelect);
    this._baseMapSelectIcon.setAttribute('aria-hidden', 'true');
  }

  onAdd(map: maplibregl.Map) {
    const _container = super.onAdd(map)
    this._print.title = 'Print'
    this._print.ariaLabel = 'Print'

    this._baseMapSelect.title = 'Change Base Map'
    this._baseMapSelect.ariaLabel = 'Change Base Map'
    return _container
  }

  _create_element<K extends keyof HTMLElementTagNameMap>(tagName: K, className?: string, container?: HTMLElement): HTMLElementTagNameMap[K] {
    const el = window.document.createElement(tagName);
    if (className !== undefined) el.className = className;
    if (container) container.appendChild(el);
    return el;
  }

}

function LegendPlaceholder(props: any) {
  return (
    <div className='legend-placeholder'>
      <div className='legend-header'>
        LEGEND
      </div>
      <div className='legend-item'>
        Properties
      </div>
      <div className='legend-item'>
        Rivers
      </div>
      <div className='legend-item'>
        Roads
      </div>
      <div className='legend-item'>
        Places
      </div>
    </div>
  )
}

class LegendControl<IControl> {
  _map: maplibregl.Map;
  _container: HTMLElement;

  constructor() {

  }

  onAdd(map: maplibregl.Map){
    this._map = map;
    this._container = document.createElement('div');
    this._container.className = 'maplibregl-ctrl maplibregl-ctrl-group mapboxgl-ctrl mapboxgl-ctrl-group';
    const divRoot = ReactDOM.createRoot(this._container)
    divRoot.render(<LegendPlaceholder />);
    return this._container;
  }

  onRemove() {
      this._container.parentNode.removeChild(this._container)
      this._map = undefined
  }

}

const checkLayerVisibility = (source_layer: string, contextLayers: ContextLayerInterface[]): boolean => {
  const contextLayer = contextLayers.find(element => element.layer_names && element.layer_names.includes(source_layer))
  if (contextLayer) {
    return contextLayer.isSelected
  }  
  return true
}

export default function Map() {
  const dispatch = useAppDispatch()
  const contextLayers = useAppSelector((state: RootState) => state.layerFilter.contextLayers)
  const isMapReady = useAppSelector((state: RootState) => state.mapStatus.isMapReady)
  const mapContainer = useRef(null);
  const map = useRef(null);
  const legendRef = useRef(null);

  useEffect(() => {
    if (!isMapReady) return;
    if (contextLayers.length === 0) return;
    if (!map.current) return;
    const _mapObj: maplibregl.Map = map.current
    const _layers = _mapObj.getStyle().layers
    for (let i=0; i < _layers.length; ++i) {
      let _layer:any = _layers[i]
      if (!('source' in _layer) || !('source-layer' in _layer) || _layer['source'] !== 'sanbi') continue
      const _is_visible = checkLayerVisibility(_layer['source-layer'], contextLayers)
      _mapObj.setLayoutProperty(_layer['id'], 'visibility', _is_visible ? 'visible' : 'none')
    }
  }, [contextLayers, isMapReady])

  useEffect(() => {
      if (map.current) return; //stops map from intializing more than once
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: `${MAP_STYLE_URL}`,
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

  return (
      <div className="map-wrap">
        <div ref={mapContainer} className="map" />
      </div>
  );
}
