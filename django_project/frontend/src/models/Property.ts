export default interface PropertyInterface {
    id: number,
    name: string,
    owner: string,
    ownerEmail?: string,
    propertyType: string,
    province: string,
    size?: number,
    organisation?: string
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
        organisation: ''
    }
    return _result
}
