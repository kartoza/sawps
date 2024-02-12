export interface ContextLayerLegendInterface {
    name: string,
    colour: string
}

export default interface ContextLayerInterface {
    id: number,
    name: string,
    layer_names?: string[],
    isSelected?: boolean,
    isExpanded?: boolean,
    legends: ContextLayerLegendInterface[]
}

export interface ContextLayerVisibilityPayload {
    id: number;
    isVisible: boolean;
}

