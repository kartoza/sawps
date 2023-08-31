import React, { useEffect, useState } from "react";
import {
  Document,
  Page,
  Text,
  View,
  StyleSheet,
  Image
} from "@react-pdf/renderer";
import axios from "axios";

// images
import logoImage from './SANBI-logo.jpg';
import mapImage from './sanbi_maps.jpg'

const FETCH_STATISTICS = '/api/statistics/';

interface ChartExportPDFProps {
  chartBase64Array: string[]; // Array of Base64 strings for the chart images
}


// these styling options are for A4 page size
const styles = StyleSheet.create({
  first_page_header: {
    backgroundColor: "black",
    padding: 10,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 0,
    height: 70
  },
  other_pages_header: {
    backgroundColor: "black",
    padding: 10,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 3,
    height: 50
  },
  logo: {
    width: 120,
    height: 35,
  },
  headerText: {
    color: "white",
    fontSize: 12,
    marginLeft: 10,
  },
  title: {
    fontSize: 16,
    marginBottom: 0,
  },
  first_page_chartImage: {
    width: "60%",
    height: "90%",
    marginLeft: 125,
    marginRight: -90
  },
  SecondPagechartImage: {
    width: "100%",
    height: "70%",
    display: "flex",
    flexDirection: "row",
    marginLeft: 70,
    marginTop: 10,
  },
  ThirdPagechartImage: {
    width: "70%",
    height: "70%",
    display: "flex",
    flexDirection: "row",
    marginLeft: 90,
    marginTop: 4,
  },
  FourthPagechartImage: {
    width: "80%",
    height: "80%",
    display: "flex",
    flexDirection: "row",
    marginLeft: 160,
    marginTop: 10,
  },
  mapImage: {
    width: "100%",
    height: "60%",
    marginBottom:-68
  },
  tableContainer: {
    marginTop: 10, 
    marginLeft: 190,
    flexDirection: "row",
    alignItems: "center",
    width: "40%",
    height: "40%",
  },
  tableRow: {
    marginTop: -161,
    marginLeft: 192,
    flexDirection: "row",
    alignItems: "center",
    width: "40%",
    height: "40%",
    marginBottom: -100,
  },
  tableCell: {
    flex: 1,
    fontSize: 8,
    fontWeight: "bold",
    color: "black",
    width: "40%",
    height: "40%",
    // borderBottom: "1px",
    // borderTop: "1px",
    // borderLeft: "1px",
    // borderRight: "1px"

  },
  firstPageCharts: {
    width: "100%",
    height: "70%",
    align: "right"
  }
});

interface Statistics {
  total_property_count: number;
  total_property_area: number;
  total_area_available_to_species: number;
}

const CreatePDFContent: React.FC<ChartExportPDFProps> = ({ chartBase64Array }) => {
  // variable for statistics
  const [statistics, setStatistics] = useState({
    total_property_count: null,
    total_property_area: null,
    total_area_available_to_species: null
  });

  const fetchStatistics = () => {
    axios.get(FETCH_STATISTICS)
      .then((response) => {
        if (response) {
          setStatistics(response.data as Statistics);
        }
      })
      .catch((error) => {
        // Handle error
        console.error(error);
      });
  };
  

  useEffect(() => {
      fetchStatistics();
  }, []);

  return (
    <Document>
      {chartBase64Array.map((chartBase64, pageIndex) => (
        <Page size="A4">
          

          {/* Map Image and Table */}
          {pageIndex === 0 && (
            <View>
              {/* Header */}
              <View style={styles.first_page_header}>
                <Image style={styles.logo} src={logoImage} />
                <View>
                  <Text style={styles.headerText}>Wildlife Population System</Text>
                  <Text style={styles.headerText}>National Summary Report</Text>
                </View>
              </View>

              {/* Map Image */}
              <Image style={styles.mapImage} src={mapImage} />

              {/* Table */}
              <View style={styles.tableContainer}>
                <Text style={styles.tableCell}>Total Property Count</Text>
                <Text style={styles.tableCell}>Total Property Area</Text>
                <Text style={styles.tableCell}>Total Property Density</Text>
                <Text style={styles.tableCell}>Total Property Area Available for Animals</Text>
              </View>
              
              <View style={styles.tableRow}>
                <Text style={styles.tableCell}>
                  {statistics.total_property_count !== null ? `${statistics.total_property_count}` : 'X'}
                </Text>
                <Text style={styles.tableCell}>
                  {statistics.total_property_area !== null ? `${statistics.total_property_area} ha` : 'X'}
                </Text>
                <Text style={styles.tableCell}>X</Text>
                <Text style={styles.tableCell}>
                  {statistics.total_area_available_to_species !== null ? `${statistics.total_area_available_to_species} ha` : 'X'}
                </Text>
              </View>

              {/* Chart Image */}
              <View>
                <Image style={styles.first_page_chartImage} src={chartBase64} />
              </View>
            </View>
          )}

          
          {/* Content for page 1 */}
          {pageIndex === 1 && (
            <View>
              {/* Header */}
              <View style={styles.other_pages_header}>
                <Image style={styles.logo} src={logoImage} />
                <View>
                  <Text style={styles.headerText}>Wildlife Population System</Text>
                  <Text style={styles.headerText}>National Summary Report</Text>
                </View>
              </View>
              {/* Chart Image */}
              <Image style={styles.SecondPagechartImage} src={chartBase64} />
            </View>
          )}

          {/* Content for page 3 */}
          {pageIndex === 2 && (
            <View>
              {/* Header */}
              <View style={styles.other_pages_header}>
                <Image style={styles.logo} src={logoImage} />
                <View>
                  <Text style={styles.headerText}>Wildlife Population System</Text>
                  <Text style={styles.headerText}>National Summary Report</Text>
                </View>
              </View>
              {/* Chart Image */}
              <Image style={styles.ThirdPagechartImage} src={chartBase64} />
            </View>
          )}

          {/* Content for page 4 */}
          {pageIndex === 3 && (
            <View>
              {/* Header */}
              <View style={styles.other_pages_header}>
                <Image style={styles.logo} src={logoImage} />
                <View>
                  <Text style={styles.headerText}>Wildlife Population System</Text>
                  <Text style={styles.headerText}>National Summary Report</Text>
                </View>
              </View>
              {/* Chart Image */}
              <Image style={styles.FourthPagechartImage} src={chartBase64} />
            </View>
          )}
  
        </Page>
      ))}
    </Document>
  );
};

export default CreatePDFContent;
