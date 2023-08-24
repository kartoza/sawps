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
    height: 110
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
    height: "95%",
    marginLeft: 125,
    marginRight: -90
  },
  line_chartImage: {
    width: "45%",
    height: "45%",
    marginLeft: 5
  },
  mapImage: {
    width: "100%",
    height: "100%",
    marginBottom:-47
  },
  tableContainer: {
    marginTop: 2, 
    marginLeft: 2,
    flexDirection: "row",
    alignItems: "center",
    width: "40%",
    height: "40%"
  },
  tableRow: {
    marginTop: -123,
    marginLeft: 0,
    flexDirection: "row",
    alignItems: "center",
    width: "40%",
    height: "40%",
    border: "none",
    marginBottom: -70,
  },
  tableCell: {
    flex: 1,
    fontSize: 8,
    fontWeight: "bold",
    color: "black",
    width: "40%",
    height: "40%"
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
  const [statistics, setStatistics] = useState<Statistics[]>([]);

  const fetchStatistics = () => {
    axios.get(FETCH_STATISTICS)
      .then((response) => {
        if (response) {
          setStatistics(response.data as Statistics[]);
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
              {statistics.map((stat, index) => (
                <View style={styles.tableRow} key={index}>
                  <Text style={styles.tableCell}>{stat.total_property_count}</Text>
                  <Text style={styles.tableCell}>{stat.total_property_area} ha</Text>
                  <Text style={styles.tableCell}>X</Text>
                  <Text style={styles.tableCell}>
                    {stat.total_area_available_to_species} ha
                  </Text>
                </View>
              ))}

              {/* Chart Image */}
              <View>
                <Image style={styles.first_page_chartImage} src={chartBase64} />
              </View>
            </View>
          )}

          

          {/* Content for Other Pages (index not 0) */}
          {pageIndex !== 0 && (
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
              <Image style={styles.line_chartImage} src={chartBase64} />
            </View>
          )}
  
        </Page>
      ))}
    </Document>
  );
};

export default CreatePDFContent;
