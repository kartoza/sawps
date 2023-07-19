
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

export enum MapTheme {
    None = "none",
    Light = "light",
    Dark = "dark"
}
