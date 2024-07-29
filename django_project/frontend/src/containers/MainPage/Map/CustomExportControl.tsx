import { IControl, PointLike, Map as MaplibreMap } from 'maplibre-gl';
import { CirclePaint, Map as MapboxMap } from 'mapbox-gl';
import { 
    MaplibreExportControl,
    defaultAttributionOptions,
	defaultMarkerCirclePaint,
	defaultNorthIconOptions,
    SizeType,
    DPIType,
    FormatType,
    UnitType,
    type ControlOptions,
    Size,
    Format,
    Unit,
    MapGeneratorBase
} from "@watergis/maplibre-gl-export";
import '@watergis/maplibre-gl-export/dist/maplibre-gl-export.css';
import LegendControl from './LegendControl';


class CustomMapGenerator extends MapGeneratorBase {
    _legendsControl: LegendControl<IControl>;
    _legendsControlRef: LegendControl<IControl>;
    /**
	 * Constructor
	 * @param map MaplibreMap object
	 * @param size layout size. default is A4
	 * @param dpi dpi value. deafult is 300
	 * @param format image format. default is PNG
	 * @param unit length unit. default is mm
	 * @param fileName file name. default is 'map'
	 */
	constructor(
		map: any,
		size: SizeType = Size.A4,
		dpi: DPIType = 300,
		format: FormatType = Format.PNG,
		unit: UnitType = Unit.mm,
		fileName = 'map',
		markerCirclePaint = defaultMarkerCirclePaint,
		attributionOptions = defaultAttributionOptions,
		northIconOptions = defaultNorthIconOptions,
        legendsControl: IControl = null
	) {
		super(
			map,
			size,
			dpi,
			format,
			unit,
			fileName,
			'maplibregl-marker',
			markerCirclePaint,
			'maplibregl-ctrl-attrib-inner',
			attributionOptions,
			northIconOptions
		);
        this._legendsControl = legendsControl as LegendControl<IControl>;
	}

	protected getRenderedMap(container: HTMLElement, style: any) {
		// Render map
		const renderMap: MaplibreMap = new MaplibreMap({
			container: container,
			style: style,
			center: this.map.getCenter(),
			zoom: this.map.getZoom(),
			bearing: this.map.getBearing(),
			pitch: this.map.getPitch(),
			interactive: false,
			preserveDrawingBuffer: true,
			fadeDuration: 0,
			attributionControl: false,
			// hack to read transfrom request callback function
			// eslint-disable-next-line
			// @ts-ignore
			// transformRequest: (this.map as unknown)._requestManager._transformRequestFn
		});

		const terrain = (this.map as any).getTerrain();
		if (terrain) {
			// if terrain is enabled, restore pitch correctly
			renderMap.setMaxPitch(85);
			renderMap.setPitch(this.map.getPitch());
		}

		// the below code was added by https://github.com/watergis/maplibre-gl-export/pull/18.
		const images = ((this.map as any).style.imageManager || {}).images || [];
		Object.keys(images).forEach((key) => {
			if (!images[key].data) return;
			renderMap.addImage(key, images[key].data);
		});
        if (this._legendsControl) {
            this._legendsControlRef = new LegendControl()
            renderMap.addControl(this._legendsControlRef, 'bottom-left')
            this._legendsControlRef.onUpdateLegends(
                this._legendsControl.getCurrentZoom(),
                this._legendsControl.getCurrentSpecies(),
                this._legendsControl.getCurrentYear(),
                this._legendsControl.getCurrentData()
            )
        }
        
		return renderMap as any;
	}

    protected renderMapPost(renderMap: any) {
		const terrain = (this.map as any).getTerrain();
		if (terrain) {
			// if terrain is enabled, set terrain for rendered map object
			renderMap.setTerrain({
				source: terrain.source,
				exaggeration: terrain.exaggeration
			});
		}
		return renderMap;
	}

    generate(): void {
        // eslint-disable-next-line
		const this_ = this;

		// see documentation for JS Loading Overray library
		// https://js-loading-overlay.muhdfaiz.com
		// eslint-disable-next-line
		// @ts-ignore
		JsLoadingOverlay.show({
			overlayBackgroundColor: '#5D5959',
			overlayOpacity: '0.6',
			spinnerIcon: 'ball-spin',
			spinnerColor: '#2400FD',
			spinnerSize: '2x',
			overlayIDName: 'overlay',
			spinnerIDName: 'spinner',
			offsetX: 0,
			offsetY: 0,
			containerID: null,
			lockScroll: false,
			overlayZIndex: 9998,
			spinnerZIndex: 9999
		});

		// Calculate pixel ratio
		const actualPixelRatio: number = window.devicePixelRatio;
		Object.defineProperty(window, 'devicePixelRatio', {
			get() {
				return this_.dpi / 96;
			}
		});
		// Create map container
		const hidden = document.createElement('div');
		hidden.className = 'hidden-map';
		document.body.appendChild(hidden);
		const container = document.createElement('div');
		container.style.width = this._toPixels(this.width);
		container.style.height = this._toPixels(this.height);
		hidden.appendChild(container);

		const style = this.map.getStyle();
		if (style && style.sources) {
			const sources = style.sources;
			Object.keys(sources).forEach((name) => {
				const src = sources[name];
				Object.keys(src).forEach((key) => {
                    // @ts-ignore
					// delete properties if value is undefined.
					// for instance, raster-dem might has undefined value in "url" and "bounds"
					if (!src[key]) delete src[key];
				});
			});
		}

		// Render map
		let renderMap = this.getRenderedMap(container, style);
        renderMap.once('idle', () => {
            this._addLegendsToMap(renderMap).then((hasLegends: boolean) => {
                if (hasLegends) {
                    renderMap.once('idle', () => {
                        this._finalizeMapRenders(renderMap, hidden, actualPixelRatio);
                    });
                } else {
                    this._finalizeMapRenders(renderMap, hidden, actualPixelRatio);
                }
            });
        });	
    }

    private _finalizeMapRenders(
        renderMap: MaplibreMap,
		hiddenDiv: HTMLElement,
		actualPixelRatio: number
    ) {
        renderMap = this.renderMapPost(renderMap);
        const markers = this._getMarkers();
        if (markers.length === 0) {
            this._exportImage(renderMap, hiddenDiv, actualPixelRatio);
        } else {
            renderMap = this.renderMarkers(renderMap as any) as any;
            renderMap.once('idle', () => {
                this._exportImage(renderMap, hiddenDiv, actualPixelRatio);
            });
        }
    }

    private _addLegendsToMap(renderMap: MaplibreMap) {
        const _this = this;
        return new Promise<boolean>((resolve) => {
            this._legendsControlRef.getContentAsCanvas().then((canvasContent: any) => {
                if (canvasContent === null) {
                    resolve(false);
                    return;
                }
                const img = canvasContent.toDataURL('image/png');
                const pixels = _this._getElementPosition(
                    renderMap,
                    'top-left',
                    0
                );
                const imgRatio = 0.75;
                const _pixels = pixels as [number, number];
                const pixels2 = [_pixels[0] + (canvasContent.width * imgRatio), _pixels[1] + (canvasContent.height * imgRatio)] as PointLike;
                const lngLat = (renderMap as MaplibreMap).unproject(pixels);
                const lngLat2 = (renderMap as MaplibreMap).unproject(pixels2);
                // Add the image to the map
                renderMap.addSource('image-source', {
                    'type': 'image',
                    'url': img,
                    'coordinates': [
                        [lngLat.lng, lngLat.lat],
                        [lngLat2.lng, lngLat.lat],
                        [lngLat2.lng, lngLat2.lat],
                        [lngLat.lng, lngLat2.lat],
                    ]
                });

                // Add an image layer
                renderMap.addLayer({
                    'id': 'image-layer',
                    'type': 'raster',
                    'source': 'image-source',
                    'paint': {
                        'raster-opacity': 1.0
                    }
                });
                resolve(true);
            });
        });
    }


    private _getMarkers() {
		return this.map.getCanvasContainer().getElementsByClassName(this.markerClassName);
	}

    /**
	 * Get element position's pixel values based on selected position setting
	 * @param renderMap Map object
	 * @param position Position of element inserted
	 * @param offset Offset value to adjust position
	 * @returns Pixels [width, height]
	 */
	private _getElementPosition(
		renderMap: MaplibreMap,
		position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right',
		offset = 0
	) {
		const containerDiv = renderMap.getContainer();
		let width = 0;
		let height = 0;

		switch (position) {
			case 'top-left':
				width = 0 + offset;
				height = 0 + offset;
				break;
			case 'top-right':
				width = parseInt(containerDiv.style.width.replace('px', '')) - offset;
				height = 0 + offset;
				break;
			case 'bottom-left':
				width = 0 + offset;
				height = parseInt(containerDiv.style.height.replace('px', '')) - offset;
				break;
			case 'bottom-right':
				width = parseInt(containerDiv.style.width.replace('px', '')) - offset;
				height = parseInt(containerDiv.style.height.replace('px', '')) - offset;
				break;
			default:
				break;
		}

		const pixels = [width, height] as PointLike;
		return pixels;
	}

    private _exportImage(
		renderMap: MaplibreMap,
		hiddenDiv: HTMLElement,
		actualPixelRatio: number
	) {
		const canvas = renderMap.getCanvas();

		const fileName = `${this.fileName}.${this.format}`;
		switch (this.format) {
			case Format.PNG:
				this._toPNG(canvas, fileName);
				break;
			case Format.JPEG:
				this._toJPEG(canvas, fileName);
				break;
			case Format.SVG:
				this._toSVG(canvas, fileName);
				break;
			default:
				console.error(`Invalid file format: ${this.format}`);
				break;
		}

		renderMap.remove();
		hiddenDiv.parentNode?.removeChild(hiddenDiv);
		Object.defineProperty(window, 'devicePixelRatio', {
			get() {
				return actualPixelRatio;
			}
		});
		hiddenDiv.remove();

		// eslint-disable-next-line
		// @ts-ignore
		JsLoadingOverlay.hide();
	}

	/**
	 * Convert canvas to PNG
	 * @param canvas Canvas element
	 * @param fileName file name
	 */
	private _toPNG(canvas: HTMLCanvasElement, fileName: string) {
		const a = document.createElement('a');
		a.href = canvas.toDataURL();
		a.download = fileName;
		a.click();
		a.remove();
	}

	/**
	 * Convert canvas to JPEG
	 * @param canvas Canvas element
	 * @param fileName file name
	 */
	private _toJPEG(canvas: HTMLCanvasElement, fileName: string) {
		const uri = canvas.toDataURL('image/jpeg', 0.85);
		const a = document.createElement('a');
		a.href = uri;
		a.download = fileName;
		a.click();
		a.remove();
	}

	/**
	 * Convert canvas to SVG
	 * @param canvas Canvas element
	 * @param fileName file name
	 */
	private _toSVG(canvas: HTMLCanvasElement, fileName: string) {
		const uri = canvas.toDataURL('image/png');

		const pxWidth = Number(this._toPixels(this.width, this.dpi).replace('px', ''));
		const pxHeight = Number(this._toPixels(this.height, this.dpi).replace('px', ''));

		const svg = `
            <svg xmlns="http://www.w3.org/2000/svg" 
            xmlns:xlink="http://www.w3.org/1999/xlink" 
            version="1.1" 
            width="${pxWidth}" 
            height="${pxHeight}" 
            viewBox="0 0 ${pxWidth} ${pxHeight}" 
            xml:space="preserve">
                <image style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-dashoffset: 0; stroke-linejoin: miter; stroke-miterlimit: 4; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;"  
            xlink:href="${uri}" width="${pxWidth}" height="${pxHeight}"></image>
            </svg>`;

		const a = document.createElement('a');
		a.href = `data:application/xml,${encodeURIComponent(svg)}`;
		a.download = fileName;
		a.click();
		a.remove();
	}

    /**
	 * Convert mm/inch to pixel
	 * @param length mm/inch length
	 * @param conversionFactor DPI value. default is 96.
	 */
	private _toPixels(length: number, conversionFactor = 96) {
		if (this.unit === Unit.mm) {
			conversionFactor /= 25.4;
		}
		return `${conversionFactor * length}px`;
	}
}


class CustomMaplibreExport extends MaplibreExportControl {
    _legendsControl: IControl;

    constructor(options: ControlOptions, legendsControl: IControl) {
        super(options);
        this._legendsControl = legendsControl;
	}

    public setLegendsControl(legendsControl: IControl) {
        this._legendsControl = legendsControl;
    }

    protected generateMap(
		map: any,
		size: SizeType,
		dpi: DPIType,
		format: FormatType,
		unit: UnitType,
		filename?: string
	) {
		const mapGenerator = new CustomMapGenerator(
			map as any,
			size,
			dpi,
			format,
			unit,
			filename,
			this.options.markerCirclePaint,
			this.options.attributionOptions,
			this.options.northIconOptions,
            this._legendsControl
		);
		mapGenerator.generate();
	}

}


export default class CustomExportControl implements IControl {
    _map: MaplibreMap;
    _exporter: MaplibreExportControl;
    _exporterContainer: HTMLElement;
    _isExporterDisplayed: boolean;
    _legends: LegendControl<IControl>;

    constructor() {
        this._exporter = new CustomMaplibreExport({
            Filename: 'sanbi_maps',
            PrintableArea: true,
            Crosshair: true
        }, null);
        this._isExporterDisplayed = false;
    }

    onAdd(map: MaplibreMap): HTMLElement {
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

    onRemove(map: MaplibreMap): void {
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

    setLegendsControl(legends: IControl) {
        this._legends = legends as LegendControl<IControl>;
        (this._exporter as CustomMaplibreExport).setLegendsControl(legends);
    }
}