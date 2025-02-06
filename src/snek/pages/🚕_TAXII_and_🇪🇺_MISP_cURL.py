import streamlit as st
import uuid

from datetime import datetime, timedelta

st.set_page_config(
    page_title="SNEK: TAXII and 🇪🇺 MISP Curl Commands",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="auto",
)

# set the initial state of session state
st.session_state.hostname = "taxii-server.example.com"
st.session_state.username = "admin"
st.session_state.password = "password"
st.session_state.https = True

st.session_state.misp_hostname = "misp.example.com"
st.session_state.misp_api_key = str(uuid.uuid4())
st.session_state.misp_base_url = "/api/v2"
st.session_state.misp_https = True

st.title("🚕 TAXII and 🇪🇺 MISP Curl Commands")
header_col1, header_col2 = st.columns(2)
with header_col1:
    st.write("""
    ## Problem: 
    You need a quick way to authenticate, and perform common tasks with TAXII Server and MISP, but you don't want to install libraries.
    """)

with header_col2:
    st.write("""
    ## Solution:
    Use the following curl commands to authenticate, and perform common tasks with TAXII Server and MISP.
    """)

# add section for user to provide hostname, username, and password
with st.container(border=True):
    
    taxii_creds, misp_creds = st.columns(2)

    with taxii_creds:

        taxii_creds.write("## 🚕 TAXII Server")

        hostname = st.session_state.get('hostname', "")
        username = st.session_state.get('username', "")
        password = st.session_state.get('password', "")
        https = st.session_state.get('https', "")

        hostname = st.text_input("", value=hostname, placeholder="Hostname")
        if hostname != "":
            st.session_state.hostname = hostname

        username = st.text_input("", value=username, placeholder="Username")
        if username != "":
            st.session_state.username = username

        password = st.text_input("", type="password", value=password, placeholder="Password")
        if password != "":
            st.session_state.password = password

        https = st.toggle("Enable HTTPS for TAXII Server", value=https)
        if https != st.session_state.get('https'):
            st.session_state.https = https

    with misp_creds:

        misp_creds.write("## 🇪🇺 MISP")

        misp_hostname = st.session_state.get('misp_hostname', "")
        misp_api_key = st.session_state.get('misp_api_key', "")
        misp_base_url = st.session_state.get('misp_base_url', "")
        misp_https = st.session_state.get('misp_https', "")

        misp_hostname = st.text_input("", value=misp_hostname, placeholder="MISP Hostname")
        if misp_hostname != "":
            st.session_state.misp_hostname = misp_hostname

        misp_base_url = st.text_input("", value=misp_base_url, placeholder="MISP Base URL")
        if misp_base_url != "":
            st.session_state.misp_base_url = misp_base_url

        misp_api_key = st.text_input("", value=misp_api_key, placeholder="MISP API Key", type="password")
        if misp_api_key != "":
            st.session_state.misp_api_key = misp_api_key

        https = st.toggle("Enable HTTPS for MISP", value=https)
        if https != st.session_state.get('https'):
            st.session_state.https = https


if st.session_state.get('hostname') != "" and st.session_state.get('username') != "" and st.session_state.get('password') != "":
    
    # add section for user to provide hostname, username, and password
    taxii_col, misp_col = st.columns(2)
    with taxii_col:
        st.write(f"""
        ## 🚕 TAXII 1.x
        ### Documentation
        * [TAXII 1.x Project](https://taxiiproject.github.io/about/)
        * [TAXII 1.x Whitepaper](https://taxiiproject.github.io/getting-started/whitepaper/)
        * [TAXII™ Version 1.1.1. Part 1: Overview](https://docs.oasis-open.org/cti/taxii/v1.1.1/taxii-v1.1.1-part1-overview.html)
        * [TAXII™ Version 1.1.1. Part 2: Services](https://docs.oasis-open.org/cti/taxii/v1.1.1/taxii-v1.1.1-part2-services.html)
        * [TAXII™ Version 1.1.1. Part 3: HTTP Protocol Binding](https://docs.oasis-open.org/cti/taxii/v1.1.1/taxii-v1.1.1-part3-http.html)
        * [TAXII™ Version 1.1.1. Part 4: XML Message Binding](https://docs.oasis-open.org/cti/taxii/v1.1.1/taxii-v1.1.1-part4-xml.html)
        * [TAXII™ Version 1.1.1. Part 5: Default Query](https://docs.oasis-open.org/cti/taxii/v1.1.1/taxii-v1.1.1-part5-query.html)
        
        """)
        with st.expander("TAXII 1.x Discovery Request"):
            message_id = st.text_input("Discovery Request Message ID", value="5267020880072015457", placeholder="Message ID")
            st.write(f"""
            ```bash
            curl \\
                --location \\
                --globoff 'https://{hostname}/ctixapi/taxii/collection/' \\
                --header 'Content-Type: application/xml' \\
                --header 'User-Agent: libtaxii.httpclient' \\
                --header 'x-taxii-accept: urn:taxii.mitre.org:message:xml:1.1' \\
                --header 'x-taxii-content-type: urn:taxii.mitre.org:message:xml:1.1' \\
                --header 'x-taxii-protocol: urn:taxii.mitre.org:protocol:https:1.0' \\
                --header 'x-taxii-services: urn:taxii.mitre.org:services:1.1' \\
                --header 'Accept: application/xml' \\
                -u '{username}:{password}' \\
                --data '<taxii_11:Discovery_Request
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:taxii="http://taxii.mitre.org/messages/taxii_xml_binding-1" 
            xmlns:taxii_11="http://taxii.mitre.org/messages/taxii_xml_binding-1.1" 
            xmlns:tdq="http://taxii.mitre.org/query/taxii_default_query-1"
            xsi:schemaLocation="http://taxii.mitre.org/messages/taxii_xml_binding-1.1" 
            message_id="{message_id}"/>'
            """
            )

        with st.expander("TAXII 1.x Collection Request"):

            message_id = st.text_input("Collection Request Message ID", value="5267020880072015457", placeholder="Message ID")
            st.write(f"""
            ```bash
            curl \\
                --location \\
                --globoff 'https://{hostname}/ctixapi/taxii/collection/' \\
                --header 'Content-Type: application/xml' \\
                --header 'User-Agent: libtaxii.httpclient' \\
                --header 'x-taxii-accept: urn:taxii.mitre.org:message:xml:1.1' \\
                --header 'x-taxii-content-type: urn:taxii.mitre.org:message:xml:1.1' \\
                --header 'x-taxii-protocol: urn:taxii.mitre.org:protocol:https:1.0' \\
                --header 'x-taxii-services: urn:taxii.mitre.org:services:1.1' \\
                --header 'Accept: application/xml' \\
                -u '{username}:{password}' \\
                --data '<taxii_11:Collection_Information_Request 
            xmlns:taxii="http://taxii.mitre.org/messages/taxii_xml_binding-1" 
            xmlns:taxii_11="http://taxii.mitre.org/messages/taxii_xml_binding-1.1" 
            xmlns:tdq="http://taxii.mitre.org/query/taxii_default_query-1" 
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
            xsi:schemaLocation="http://taxii.mitre.org/messages/taxii_xml_binding-1.1" 
            message_id="{message_id}"/>'
            ```
            """)

        with st.expander("TAXII 1.x Poll Request"):
            collection_name = st.text_input("", value="Test Collection", placeholder="Collection Name")
            message_id = st.text_input("Poll Request Message ID", value="5267020880072015457", placeholder="Message ID")
            start_ts = st.text_input("", value="2025-02-01T00:00:00.000Z", placeholder="Start Timestamp")
            end_ts = st.text_input("", value="2025-02-01T23:59:59.999Z", placeholder="End Timestamp")
            response_type = st.selectbox("", options=["FULL", "DIFF"], index=0)
            allow_asynch = st.selectbox("", options=["true", "false"], index=0)
            st.write(f"""
            ```bash
            curl \\
                --location \\
                --globoff 'https://{hostname}/ctixapi/taxii/poll/' \\
                --header 'Content-Type: application/xml' \\
                --header 'User-Agent: libtaxii.httpclient' \\
                --header 'x-taxii-accept: urn:taxii.mitre.org:message:xml:1.1' \\
                --header 'x-taxii-content-type: urn:taxii.mitre.org:message:xml:1.1' \\
                --header 'x-taxii-protocol: urn:taxii.mitre.org:protocol:https:1.0' \\
                --header 'x-taxii-services: urn:taxii.mitre.org:services:1.1' \\
                --header 'Accept: application/xml' \\
                -u '{username}:{password}' \\
                --data '<taxii_11:Poll_Request 
            xmlns:taxii_11="http://taxii.mitre.org/messages/taxii_xml_binding-1.1" 
            message_id="{message_id}" 
            collection_name="{collection_name}">
            <taxii_11:Exclusive_Begin_Timestamp>{start_ts}</taxii_11:Exclusive_Begin_Timestamp>
            <taxii_11:Inclusive_End_Timestamp>{end_ts}</taxii_11:Inclusive_End_Timestamp>
            <taxii_11:Poll_Parameters allow_asynch="{allow_asynch}">
                <taxii_11:Response_Type>{response_type}</taxii_11:Response_Type>
                <taxii_11:Content_Binding binding_id="urn:stix.mitre.org:xml:1.2"/>
            </taxii_11:Poll_Parameters>
            </taxii_11:Poll_Request>
            '
            ```
            """)

        with st.expander("TAXII 1.x Poll Fulfilment Request"):
            st.write(f"""
            ```bash
            curl \\
                --location \\
                --globoff 'https://{hostname}/ctixapi/taxii/poll/' \\
                --header 'Content-Type: application/xml' \\
                --header 'User-Agent: libtaxii.httpclient' \\
                --header 'x-taxii-accept: urn:taxii.mitre.org:message:xml:1.1' \\
                --header 'x-taxii-content-type: urn:taxii.mitre.org:message:xml:1.1' \\
                --header 'x-taxii-protocol: urn:taxii.mitre.org:protocol:https:1.0' \\
                --header 'x-taxii-services: urn:taxii.mitre.org:services:1.1' \\
                --header 'Accept: application/xml' \\
                -u '{username}:{password}' \\
                --data '<taxii_11:Poll_Fulfillment 
                xmlns:taxii_11="http://taxii.mitre.org/messages/taxii_xml_binding-1.1" 
                message_id="42158" 
                collection_name="ctix.ipr" result_id="85eeaa13-70af-40ce-857a-e3d209ad0471" result_part_number="2">
                </taxii_11:Poll_Fulfillment>'
            ```
            """)

        # add a divider
        st.divider()

        # TAXII 2.0
        st.write("""
        ## 🚕 TAXII 2.x

        ### Documentation 
        * [TAXII 2.1 Specification](https://docs.oasis-open.org/cti/taxii/v2.1/os/taxii-v2.1-os.html)
        * [TAXII 2.1 Interoperability Test Document Version 1.0](https://docs.oasis-open.org/cti/taxii-2.1-interop/v1.0/taxii-2.1-interop-v1.0.html)
        * [STIX 2.1 Interoperability Test Document Version 1.0](https://docs.oasis-open.org/cti/stix-2.1-interop/v1.0/stix-2.1-interop-v1.0.html)
        
        """)

        # TAXII 2.x Discovery Request
        with st.expander("TAXII 2.x Discovery Request"):
            st.write(f"""
            ```bash
            curl \\
                --location \\
                --globoff \\
                'https://{hostname}/ctixapi/ctix21/taxii2/' \\
                --header 'Accept: application/taxii+json;version=2.1' \\
                --header 'Content-Type: application/taxii+json;version=2.1' \\
                -u '{username}:{password}'
            ```
            """)

        # TAXII 2.x Collection Request
        with st.expander("TAXII 2.x Collection Request"):

            st.write(f"""
            ```bash
            curl \\
                --location \\
                --globoff \\
                'https://{hostname}/ctixapi/ctix21/collections/' \\
                --header 'Accept: application/taxii+json;version=2.1' \\
                --header 'Content-Type: application/taxii+json;version=2.1' \\
                -u '{username}:{password}'
            ```
            """)

        # TAXII 2.x Object Request
        with st.expander("TAXII 2.x Object Request"):
            collection_id = st.text_input("Collection ID", "5fa2ed32-c1e6-440a-a5ef-cede37982da3")
            added_after = st.text_input("Added After", "2025-01-01T00:00:00.000000Z")
            st.write(f"""
            curl \\
                --location \\
                --globoff \\
                'https://{hostname}/ctixapi/ctix21/collections/{collection_id}/objects/?added_after={added_after}' \\
                --header 'Accept: application/taxii+json;version=2.1' \\
                --header 'Content-Type: application/taxii+json;version=2.1' \\
                -u '{username}:{password}'
            """)

    with misp_col:

        misp_hostname = st.session_state.get('misp_hostname', "")
        misp_api_key = st.session_state.get('misp_api_key', "")
        misp_base_url = st.session_state.get('misp_base_url', "").strip('/')
        misp_https = st.session_state.get('misp_https', "")

        if misp_https:
            misp_url = f"https://{misp_hostname}/{misp_base_url}"
        else:
            misp_url = f"http://{misp_hostname}/{misp_base_url}"


        st.write('''
        ## 🇪🇺 MISP

        ### Documentation

        * [MISP OpenAPI Spec](https://www.misp-project.org/openapi/)

        ### Curl Commands
        ''')

        # Event Operations
        with st.expander("Event Operations"):

            start_date = st.date_input("Event Start Date", datetime.now() - timedelta(days=1))
            end_date = st.date_input("Event End Date", value=datetime.now())

            st.write(f"""
            ```bash

            # search for events
            curl -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                "{misp_api_key}/events/index.json"
            
            # search for events with filters
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "returnFormat": "json",
                "published": true,
                "threat_level_id": "4",
                "date_from": "{start_date}",
                "date_to": "{end_date}"
                }}' \\
                "{misp_api_key}/events/restSearch"
            ```
            """)

        # Attributes
        with st.expander("Attributes Operations"):

            st.write(f"""
            ```bash
            # Search for attributes
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                    "returnFormat": "json",
                    "type": "ip-dst",
                    "value": "8.8.8.8"
                }}' \\
                "{misp_api_key}/attributes/restSearch"
            ```
            """)

        # Event Operations
        with st.expander("Event Operations"):
            
            st.write(f"""
            ```bash
            # Create new event
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "info": "Suspicious Activity Report",
                "distribution": "0",
                "threat_level_id": "2",
                "analysis": "0"
                }}' \\
                "{misp_api_key}/events/add"
            
            # Get specific event
            curl -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/events/view/1234"
            # Update event
            curl -X PUT \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "Event": {{
                        "id": "1234",
                        "analysis": "1",
                        "threat_level_id": "3"
                    }}
                }}' \\
                "{misp_api_key}/events/1234"
            
            # Delete event
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/events/delete/1234"

            ```
            """)

        with st.expander("Attribute Operations"):
            
            st.write(f"""
            ```bash
            # Add attribute to event
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "event_id": "1234",
                "type": "ip-dst",
                "category": "Network activity",
                "value": "10.0.0.1",
                "comment": "C2 server"
                }}' \\
                "{misp_api_key}/attributes/add/1234"

            # Update attribute
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "type": "ip-dst",
                "value": "10.0.0.1",
                "comment": "Updated C2 server info"
                }}' \\
                "{misp_api_key}/attributes/edit/5678"
                
            # Delete attribute
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/attributes/delete/5678"

            ```
            """)

        with st.expander("Tag Operations"):
            
            st.write(f"""
            ```bash
            # Create new tag
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "name": "APT:GROUP-123",
                "colour": "#ff0000",
                "exportable": true
                }}' \\
                "{misp_api_key}/tags/add"
            # Add tag to event
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/events/addTag/1234/APT:GROUP-123"
            # Remove tag from event
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/events/removeTag/1234/APT:GROUP-123"

            ```
            """)

        with st.expander("Sharing Operations"):
            
            st.write(f"""
            ```bash
            # List sharing groups
            curl -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/sharing_groups/index"
            
            # Create sharing group
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "name": "Incident Response Team",
                "releasability": "Restricted",
                "description": "IR team sharing group"
                }}' \\
                "{misp_api_key}/sharing_groups/add"

            ```
            """)

        with st.expander("User Operations"):
            
            st.write(f"""
            ```bash
            
            # List users
            curl -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/admin/users"

            # Add user (requires admin)
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "email": "analyst@organization.com",
                "org_id": "1",
                "role_id": "3"
                }}' \\
                "{misp_api_key}/admin/users/add"
                
            # Delete user (requires admin)
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/admin/users/delete/1234"
            
            ```
            """)

        with st.expander("Feed Operations"):
            
            st.write(f"""
            ```bash
            # List feeds
            curl -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/feeds/index"

            # Enable feed
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/feeds/enable/1234"

            # Fetch feed
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/feeds/fetchFromFeed/1234"
            ```
            """)

        with st.expander("Sighting Operations"):
            
            st.write(f"""
            ```bash

            # Add sighting
            curl -X POST \\
                -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                -H "Content-Type: application/json" \\
                -d '{{
                "value": "8.8.8.8",
                "source": "Internal Monitoring",
                "type": "0"
                }}' \\
                "{misp_api_key}/sightings/add"

            # Get sightings for a specific attribute
            curl -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/sightings/listSightings/attribute/5678"
            
            ```
            """)

        with st.expander("Export Operations"):

            st.write(f"""
            ```bash 
            # Export all events as STIX
            curl -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/events/stix/download"
            
            # Export specific event as CSV
            curl -H "Authorization: {misp_api_key}" \\
                -H "Accept: application/json" \\
                "{misp_api_key}/events/csv/download/1234"
            ```
            """)



else:
    st.warning("Please enter credentials")