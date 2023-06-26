import React from 'react';
import ReactDOM from "react-dom/client";
import {IControl, Map as MapLibreMap} from 'maplibre-gl';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Loading from '../../../components/Loading';

interface LoadingIndicatorControlInterface {
    label?: string;
}

export default class LoadingIndicatorControl implements IControl {
    _container: HTMLElement;
    _map: MapLibreMap;
    _label?: string;

    constructor(opt: LoadingIndicatorControlInterface) {
        this._label = opt.label ? opt.label : 'Processing...'
    }
  
    onAdd(map: MapLibreMap): HTMLElement {
        let ctrl = this
        ctrl._map = map
        ctrl._container = document.createElement('div')
        ctrl._container.className = 'maplibregl-ctrl';
        const divRoot = ReactDOM.createRoot(ctrl._container)
        divRoot.render(
            <Card>
                <CardContent sx={{ flex: '1 0 auto', padding: '10px !important' }}>
                    <Loading label={ctrl._label} />
                </CardContent>
            </Card>
        )
        return ctrl._container
    }

    onRemove(map: MapLibreMap): void {
      this._container.parentNode.removeChild(this._container)
      this._map = undefined
    }
  }