import {
    IControl,
    Map as MapBoxGLMap,
} from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw';


interface ControlButtonInterface {
    on: string;
    action: () => void;
    classes: string[];
    content: Element | string;
    elButton?: Element;
}


interface CustomDrawControlInterface {
    draw: MapboxDraw;
    buttons: ControlButtonInterface[];
}


export default class CustomDrawControl implements IControl {

    _map: MapBoxGLMap;
    _elContainer: HTMLElement;
    _draw: MapboxDraw;
    _buttons: ControlButtonInterface[];
    _onAddOrig: (map: MapBoxGLMap) => HTMLElement;
    _onRemoveOrig: (map: MapBoxGLMap) => any;

    constructor(opt: CustomDrawControlInterface) {
        let ctrl = this
        ctrl._draw = opt.draw;
        ctrl._buttons = opt.buttons || [];
        ctrl._onAddOrig = opt.draw.onAdd;
        ctrl._onRemoveOrig = opt.draw.onRemove;
    }

    onAdd(map: MapBoxGLMap): HTMLElement {
        let ctrl = this;
        ctrl._map = map;
        ctrl._elContainer = ctrl._onAddOrig(map);
        ctrl._buttons.forEach((b) => {
            ctrl.addButton(b);
        });
        return ctrl._elContainer;
    }

    onRemove(map: MapBoxGLMap): void {
        let ctrl = this;
        ctrl._buttons.forEach((b) => {
            ctrl.removeButton(b);
        });
        ctrl._onRemoveOrig(map);
    }

    addButton(opt: ControlButtonInterface) {
        let ctrl = this;
        var elButton = document.createElement('button');
        elButton.className = 'mapbox-gl-draw_ctrl-draw-btn';
        if (opt.classes instanceof Array) {
          opt.classes.forEach((c) => {
            elButton.classList.add(c);
          });
        }
        if (opt.content) {
          if (opt.content instanceof Element) {
            elButton.appendChild(opt.content);
          } else {
            elButton.innerHTML = opt.content
          }
        }
        elButton.addEventListener(opt.on, opt.action);
        ctrl._elContainer.appendChild(elButton);
        opt.elButton = elButton;
    }

    removeButton(opt: ControlButtonInterface) {
        opt.elButton.removeEventListener(opt.on, opt.action);
        opt.elButton.remove();
    }

    getMapBoxDraw() {
        return this._draw
    }
}
