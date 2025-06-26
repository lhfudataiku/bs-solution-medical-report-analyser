import streamlit.components.v1 as components
import os

# Point to the location of the built frontend files
_RELEASE = True # Set to False for development
if not _RELEASE:
    _dataiku_filter_listener = components.declare_component(
        "dataiku_filter_listener",
        url="http://localhost:3001", # URL of the dev server
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _dataiku_filter_listener = components.declare_component("dataiku_filter_listener", path=build_dir)

def dataiku_filter_listener(key=None):
    """Create a new instance of our Dataiku filter listener component."""
    # The component will send its value back to Streamlit, which we can capture.
    # The default value is None. It will be updated when a filter event occurs.
    component_value = _dataiku_filter_listener(key=key, default=None)
    return component_value