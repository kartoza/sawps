import { UserInfo } from "../services/api";

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
 * Check if user has a Data Consumer role
 * @param userInfo user info from API
 * @returns True if user has group/role of Data Consumer
 */
export function isDataConsumer(userInfo: UserInfo) {
  if (!userInfo?.user_roles) return false;
  if (userInfo.user_roles.includes('Super user')) return false;
  const dataConsumers = new Set([
    "National data consumer",
      "Provincial data consumer"
  ])
  return userInfo.user_roles.some(userRole => dataConsumers.has(userRole))
}


/**
 * Check if user has a Data Scientiest role
 * @param userInfo user info from API
 * @returns True if user has group/role of Data Consumer
 */
export function isDataScientiest(userInfo: UserInfo) {
  if (!userInfo?.user_roles) return false;
  if (userInfo.user_roles.includes('Super user')) return false;
  const dataScientiests = new Set([
    "National data scientist",
      "Provincial data scientist"
  ])
  return userInfo.user_roles.some(userRole => dataScientiests.has(userRole))
}

