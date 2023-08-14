export const REQUIRED_FIELD_ERROR_MESSAGE = 'This field is required'

export const getErrorMessage = (errorMessages: any, key: string) => {
    if (errorMessages[key] !== undefined && errorMessages[key] !== '') return errorMessages[key]
    return REQUIRED_FIELD_ERROR_MESSAGE
}
