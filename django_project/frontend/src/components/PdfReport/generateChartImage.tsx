import React, { useEffect, useRef, useState } from "react";
import { Chart, LinearScale } from "chart.js";
import CreatePDFContent from ".";
import { PDFDownloadLink } from "@react-pdf/renderer";
import { Button } from "@mui/material";

// import chart componenents to be rendered here
import FirstPageCharts from "./FirstPageContent";
import SecondPageCharts from "./SecondPageContainer";
import ThirdPageCharts from "./ThirdPageContainer";

import html2canvas from "html2canvas";

Chart.register(LinearScale);

const GenerateChartImages: React.FC = () => {

  // define refs to capture charts
  const firstPageRefs = useRef(null);
  const secondPageRefs = useRef(null);
  const thirdPageRefs = useRef(null);

  // define variables to save charts base64 strings
  const [charts, setCharts] = useState([]);

  // manage the preview modal
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [showChartsDiv, setShowChartsDiv] = useState(false); 
  const [loadingCharts, setLoadingCharts] = useState(true); 

  const [show3rdPageChartsDiv, set3rdPageShowChartsDiv] = useState(true);

    useEffect(() => {
        const timeout = setTimeout(() => {
          set3rdPageShowChartsDiv(false);
        }, 5000); // Set the duration in milliseconds

        return () => clearTimeout(timeout); // Clear the timeout when the component unmounts
    }, []);

  useEffect(() => {

    // Simulating fetching of charts data
    setTimeout(() => {
      setLoadingCharts(true);
    }, 5000); 
  }, []);

  const openModal = async () => {
    setShowChartsDiv(true);
    set3rdPageShowChartsDiv(true)
    setIsModalOpen(true);
  
    // Only fetch and generate charts if charts are not loaded yet
    if (charts.length === 0) {
      setTimeout(async () => {
        setLoadingCharts(true);
  
        // retrieve the charts refs as canvas
        const first_page_canvas = await html2canvas(firstPageRefs.current);
        const second_page_canvas = await html2canvas(secondPageRefs.current);
        const third_page_canvas = await html2canvas(thirdPageRefs.current);

        // Convert the canvas to base64 strings
        const base64StringsArray = [];

        if (first_page_canvas.toDataURL) {
            const first_page_charts = first_page_canvas.toDataURL('image/png');
            base64StringsArray.push(first_page_charts);
        }

        if (second_page_canvas.toDataURL) {
            const second_page_charts = second_page_canvas.toDataURL('image/png');
            base64StringsArray.push(second_page_charts);
        }

        if (third_page_canvas.toDataURL) {
            const third_page_charts = third_page_canvas.toDataURL('image/png');
            base64StringsArray.push(third_page_charts);
        }
  
        // Update the state with the entire array of base64 strings
        setCharts(base64StringsArray);
  
        // Hide the div after generating charts
        setShowChartsDiv(false);
        set3rdPageShowChartsDiv(false)
        setLoadingCharts(false);
      }, 3000);
    } else {
      set3rdPageShowChartsDiv(false)
      setShowChartsDiv(false); // Hide the div if charts are already loaded
    }
  };
  

  const closeModal = () => {
    setShowChartsDiv(false);
    setIsModalOpen(false);
  };

  return (
    <div>
      {/* first page charts */}
      <div ref={firstPageRefs} style={{ display: showChartsDiv ? 'block' : 'none' }}>
        <FirstPageCharts />
      </div>
      {/* second page charts */}
      <div ref={secondPageRefs} style={{ display: showChartsDiv ? 'block' : 'none' }}>
          <SecondPageCharts />
      </div>
      {/* third page charts */}
      <div ref={thirdPageRefs} style={{ display: show3rdPageChartsDiv ? 'block' : 'none' }}>
          <ThirdPageCharts />
      </div>

      <div className="export-button-container">
        <Button onClick={openModal} variant="contained" color="primary">
          Export Charts
        </Button>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <h2>Preview</h2>
            {loadingCharts ? (
              <div>Loading charts...</div>
            ) : (
              <div className="charts-container">
                {charts.map((chart, index) => (
                  <img
                      key={index}
                      src={chart}
                      alt={`Chart ${index}`}
                      style={{  ...(index === 0 ? { width: '100%', height: 'auto'} : {}) }}
                  />
              ))}
              </div>
            )}

            <div className="modal-buttons">
              <Button onClick={closeModal} variant="contained" style={{ backgroundColor: '#FAA755' }}>
                Close
              </Button>
              {charts.length > 0 && (
                <PDFDownloadLink
                  document={<CreatePDFContent chartBase64Array={charts} />}
                  fileName="national_report.pdf"
                >
                  {({ loading }) =>
                    loading ? (
                      <Button variant="contained" color="primary">
                        Generating Report...
                      </Button>
                    ) : (
                      <Button variant="contained" color="primary">
                        Download PDF
                      </Button>
                    )
                  }
                </PDFDownloadLink>
              )}
            </div>
          </div>
        </div>
      )}

      <style>
        {`
          .modal {
            display: ${isModalOpen ? 'block' : 'none'};
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
          }

          .export-button-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1001;
          }

          .modal-buttons button {
            font-weight: bold;
          }

          .modal-content {
            background-color: white;
            width: 50%;
            max-width: 600px;
            margin: 100px auto;
            padding: 20px;
            max-height: none;
          }

          .charts-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
            max-height: 60vh;

            overflow-y: auto;
          }

          .modal-buttons {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-top: 10px;
          }

          .modal-buttons button:nth-child(1) {
            background-color: #70B276;
            margin-right: 10px;
          }
        `}
      </style>
    </div>
  );
}

export default GenerateChartImages;
