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
    legends: ContextLayerLegendInterface[],
    description?: string
}

export interface ContextLayerVisibilityPayload {
    id: number;
    isVisible: boolean;
}


export const NGI_AERIAL_IMAGERY_LAYER = 'NGI Aerial Imagery'
export const NGI_LAYER_GROUP = ['Properties', NGI_AERIAL_IMAGERY_LAYER]
