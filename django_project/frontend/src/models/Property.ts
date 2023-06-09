import ParcelInterface from "./Parcel"

export default interface PropertyInterface {
    id: number,
    name: string,
    owner: string,
    ownerEmail?: string,
    propertyType: string,
    propertyTypeId?: number,
    province: string,
    provinceId?: number,
    size?: number,
    organisation?: string,
    organisationId?: number,
    parcels?: ParcelInterface[]
}

export const createNewProperty = ():PropertyInterface => {
    let _result:PropertyInterface = {
        id: 0,
        name: '',
        owner: '',
        ownerEmail: '',
        propertyType: '',
        province: '',
        size: 0,
        organisation: '',
        parcels: [],
        propertyTypeId: 0,
        provinceId: 0,
        organisationId: 0
    }
    return _result
}
