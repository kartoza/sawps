import {UserInfo} from "../services/api";

/**
 * Change string to singular
 */
export function toSingular(str: string) {
    let singularStr = str
    if (str[str.length - 1] === 's') {
      singularStr = singularStr.substring(0, singularStr.length - 1);
    }
    return singularStr
  }

  /**
   * Capitalize string
   */
  export function capitalize(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1)
  }

  /**
   * Get title from string
   */
  export function getTitle(key: string) {
    return  key.split('_')
      .map((part) => capitalize(part))
      .join(' ').trim()
  }

  /**
   * Get file type from layer_type and filename
   */
  export function getFileType(layer_type: string, filename: string): string {
    let extension = filename.split('.').pop()
    let file_type = ''
    if (layer_type === 'GEOJSON')
      file_type = extension==='geojson'?'application/geo+json':'application/json'
    else if (layer_type === 'GEOPACKAGE')
      file_type = 'application/geopackage+sqlite3'
    else if (layer_type === 'SHAPEFILE')
      file_type = 'application/zip'

    return file_type
  }

export const delay = (ms: number) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Checks if the current URL corresponds to the map page
 */
export const isMapDisplayed = () => {
  const currentUrl = window.location.href;
  return currentUrl.endsWith('/map') || currentUrl.endsWith('/map/')
}


/**
 * Capitalize each word in string
 */
export function capitalizeSentence(str: string) {
  return str.split(' ').map((word) => capitalize(word)).join(' ').trim()
}


/**
 * Format datetime to text
 * @param dateTime 
 * @param defaultText text value if dateTime is null
 * @returns formatted datetime in DD/MM/YYYY hh:mm:ss
 */
export function displayDateTime(dateTime: Date, defaultText?: string) {
  if (dateTime == null && defaultText) return defaultText;
  if (dateTime == null && !defaultText) return ' ';
  let _date = new Date(dateTime)
  return _date.toLocaleDateString('en-gb', { year:"numeric", month:"numeric", day:"numeric"}) + ' ' +
    _date.toLocaleTimeString('en-gb', {hour:"numeric", minute:"numeric", second:"numeric"})
}


/**
 * Check whether user is a data consumer
 * @param userInfo: user info object from /user-info endpoint
 */
export function isDataConsumer(userInfo: UserInfo) {
    if (!userInfo?.user_permissions) return false;
    return userInfo.user_permissions.includes('Can view report as data consumer')
}
