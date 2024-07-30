import { IControl, PointLike, Map as MaplibreMap } from 'maplibre-gl';
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


/**
 * Class to store canvas data from LegendsControl
 */
class CanvasData {
	image: any;
	coords: PointLike;
	scaledWidth: number;
	scaledHeight: number;

	constructor(image: any, coords: PointLike, scaledWidth: number, scaledHeight: number) {
		this.image = image;
		this.coords = coords;
		this.scaledWidth = scaledWidth;
		this.scaledHeight = scaledHeight;
	}
	
}


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
	 * @param legendsControl original LegendControl
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
        legendsControl: LegendControl<IControl> = null
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
        this._legendsControl = legendsControl;
	}

	/**
	 * Clone the map object
	 * @param container hidden container
	 * @param style original map style
	 * @returns MaplibreMap, cloned map object
	 */
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
		// clone the existing legendsControl
        if (this._legendsControl) {
            this._legendsControlRef = new LegendControl(true);
            renderMap.addControl(this._legendsControlRef, 'bottom-left');
            this._legendsControlRef.updateLegendsFromOther(this._legendsControl);
			this._legendsControlRef.onThemeChanged(this._legendsControl._currentTheme);
        }
        
		return renderMap as any;
	}

	/**
	 * Post render method
	 * @param renderMap, MaplibreMap
	 * @returns MaplibreMap
	 */
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

	/**
	 * Generate screenshot from a map
	 */
    generate(): void {
        // eslint-disable-next-line
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
		const this_ = this;
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

		// Render map, need to use idle event to wait for layers to be loaded
		let renderMap = this.getRenderedMap(container, style);
        renderMap.once('idle', () => {
            this._addLegendsToMap(renderMap).then((canvasData: CanvasData) => {
				renderMap = this.renderMapPost(renderMap);
				const markers = this._getMarkers();
				if (markers.length === 0) {
					this._exportImage(renderMap, hidden, actualPixelRatio, canvasData);
				} else {
					renderMap = this.renderMarkers(renderMap as any) as any;
					renderMap.once('idle', () => {
						this._exportImage(renderMap, hidden, actualPixelRatio, canvasData);
					});
				}
            });
        });	
    }

	/**
	 * Add legends image layer into renderMap
	 * @param renderMap MaplibreMap
	 * @returns Promise<CanvasData>, True if there is legends layer
	 */
    private _addLegendsToMap(renderMap: MaplibreMap) {
        const _this = this;
        return new Promise<CanvasData>((resolve) => {
            this._legendsControlRef.getContentAsCanvas().then((canvasContent: any) => {
                if (canvasContent === null) {
                    resolve(null);
                    return;
                }
                const pixels = _this._getElementPosition(
                    renderMap,
                    'bottom-left',
                    10
                );
                var imgRatio = window.devicePixelRatio || 1;
				imgRatio = imgRatio * 0.75;
                const _pixels = pixels as [number, number];
				// calculate coordinate from top-left image bounds
                const pixels2 = [_pixels[0], _pixels[1] - (canvasContent.height * imgRatio)] as PointLike;
                resolve(new CanvasData(canvasContent, pixels2, canvasContent.width * imgRatio, canvasContent.height * imgRatio));
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
		let mapCanvas = renderMap.getCanvas();
		let refWidth = mapCanvas.width;
		let refHeight = mapCanvas.height;
		let width = 0;
		let height = 0;

		switch (position) {
			case 'top-left':
				width = 0 + offset;
				height = 0 + offset;
				break;
			case 'top-right':
				width = refWidth - offset;
				height = 0 + offset;
				break;
			case 'bottom-left':
				width = 0 + offset;
				height = refHeight - offset;
				break;
			case 'bottom-right':
				width = refWidth - offset;
				height = refHeight - offset;
				break;
			default:
				break;
		}

		const pixels = [width, height] as PointLike;
		return pixels;
	}

	/**
	 * Export renderMap based on selected format.
	 * @param renderMap Map object
	 * @param hiddenDiv hidden container
	 * @param actualPixelRatio device pixel ratio
	 */
    private _exportImage(
		renderMap: MaplibreMap,
		hiddenDiv: HTMLElement,
		actualPixelRatio: number,
		legendsCanvasData: CanvasData
	) {
		const mapCanvas = renderMap.getCanvas();
		var canvas = null;
		if (legendsCanvasData) {
			const combinedCanvas = document.createElement('canvas');
			combinedCanvas.width = mapCanvas.width;
			combinedCanvas.height = mapCanvas.height;
			const combinedCtx = combinedCanvas.getContext('2d');
			combinedCtx.drawImage(mapCanvas, 0, 0, combinedCanvas.width, combinedCanvas.height);
			// draw legends canvas
			const legendsCoords = legendsCanvasData.coords as [number, number];
			combinedCtx.drawImage(legendsCanvasData.image, legendsCoords[0], legendsCoords[1], legendsCanvasData.scaledWidth, legendsCanvasData.scaledHeight);
			canvas = combinedCanvas;
		} else {
			canvas = mapCanvas;
		}

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
    _legendsControl: LegendControl<IControl>;

    constructor(options: ControlOptions, legendsControl: LegendControl<IControl>) {
        super(options);
        this._legendsControl = legendsControl;
	}

    public setLegendsControl(legendsControl: LegendControl<IControl>) {
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

	public isDisplayed() {
		return this.exportContainer.style.display !== 'none';
	}
}


export default class CustomExportControl implements IControl {
    _map: MaplibreMap;
    _exporter: CustomMaplibreExport;
    _exporterContainer: HTMLElement;

    constructor() {
        this._exporter = new CustomMaplibreExport({
            Filename: 'sanbi_maps',
            PrintableArea: true,
            Crosshair: true
        }, null);
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
        if (!this._exporter.isDisplayed()) {
            // seems this will trigger onDocumentClick inside the MaplibreExportControl
            // so timeout to the rescue
            setTimeout(() => {
                let _buttonControl = this._exporterContainer.getElementsByClassName('maplibregl-export-control').item(0) as HTMLButtonElement
                _buttonControl.click()
            }, 100)
        }
    }

    setLegendsControl(legends: LegendControl<IControl>) {
        (this._exporter as CustomMaplibreExport).setLegendsControl(legends);
    }
}