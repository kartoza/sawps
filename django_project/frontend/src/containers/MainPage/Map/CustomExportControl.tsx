import { IControl, Map as MapLibreMap } from 'maplibre-gl';
import { MaplibreExportControl} from "@watergis/maplibre-gl-export";
import '@watergis/maplibre-gl-export/dist/maplibre-gl-export.css';

export default class CustomExportControl implements IControl {
    _map: MapLibreMap;
    _exporter: MaplibreExportControl;
    _exporterContainer: HTMLElement;
    _isExporterDisplayed: boolean;

    constructor() {
        this._exporter = new MaplibreExportControl({
            Filename: 'sanbi_maps',
            PrintableArea: true,
            Crosshair: true
        })
        this._isExporterDisplayed = false;
    }

    onAdd(map: MapLibreMap): HTMLElement {
        this._map = map
        this._exporterContainer = this._exporter.onAdd(map as any)
        let _buttonControl = this._exporterContainer.getElementsByClassName('maplibregl-export-control').item(0) as HTMLButtonElement
        // hide current button from control group
        _buttonControl.style.display = 'none'
        // remove pdf export (accuracy not good)
        let _selectChildren = this._exporterContainer.getElementsByTagName('select')
        if (_selectChildren && _selectChildren.length) {
            let _formatTypeSelect = null
            for (let child_idx=0;child_idx<_selectChildren.length;++child_idx) {
                if (_selectChildren[child_idx].getAttribute('id') === 'mapbox-gl-export-format-type') {
                    _formatTypeSelect = _selectChildren[child_idx] as HTMLSelectElement
                    break
                }
            }
            if (_formatTypeSelect) {
                for (let i=0; i<_formatTypeSelect.length; i++) {
                    if (_formatTypeSelect.options[i].value == 'pdf')
                        _formatTypeSelect.remove(i);
                }
            }
        }
        return this._exporterContainer
    }

    onRemove(map: MapLibreMap): void {
        this._exporter.onRemove()   
    }

    showExporter(): void {
        if (!this._isExporterDisplayed) {
            // seems this will trigger onDocumentClick inside the MaplibreExportControl
            // so timeout to the rescue
            setTimeout(() => {
                let _buttonControl = this._exporterContainer.getElementsByClassName('maplibregl-export-control').item(0) as HTMLButtonElement
                _buttonControl.click()
            }, 100)
            this._isExporterDisplayed = true
        } else {
            this._isExporterDisplayed = false
        }
        
    }
}