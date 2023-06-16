
export enum MapSelectionMode {
    None = "none",
    Property = "property",
    Parcel = "parcel",
    Digitise = "digitise",
    ParcelJSON = "parcelJSON"
}

export interface MapEventInterface {
    id: string;
    name: string;
    date: number;
    payload?: string[];
}
