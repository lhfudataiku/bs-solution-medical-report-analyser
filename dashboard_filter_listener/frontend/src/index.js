import { Streamlit, RenderData } from "streamlit-component-lib"

// Function to send data back to the Python script
function sendFilterValue(data) {
  Streamlit.setComponentValue(data)
}

// Listen for messages from the Dataiku Dashboard
window.addEventListener("message", (event) => {
  // Check if the message is a filter change event
  if (event.data && event.data.type === 'filters') {
    console.log("Filter event received from Dataiku:", event.data);
    // Send the filter data to the Streamlit Python backend
    sendFilterValue(event.data)
  }
});

// Initial render function (can be minimal)
function onRender(event) {
    // Tell Streamlit we're ready to start receiving data
    Streamlit.setFrameHeight(50) // Set a small height for this invisible component
}

// Render the component
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()