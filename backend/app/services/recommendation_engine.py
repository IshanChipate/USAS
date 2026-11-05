"""
Comprehensive, evidence-grounded urban sustainability recommendations for Maharashtra cities.
Integrates local municipal context, phased roadmaps (0-6m, 6-18m, 18-36m), spatial feasibility,
official policy citations, FAISS RAG evidence retrieval, and optional Gemini enhancement.
"""

import json
import math
from pathlib import Path
from typing import List, Dict, Any, Optional

from .scoring_engine import get_city_score, load_scoring_config
from .problem_detector import classify_indicators, identify_problem_areas, INDICATORS
from .spatial_analysis import get_spatial_readiness, MAHARASHTRA_CITY_COORDINATES
from .data_loader import normalize_city_name

# Municipal and geographical context for Maharashtra cities
CITY_LOCAL_CONTEXT = {
    "pune": {
        "authority": "Pune Municipal Corporation (PMC)",
        "context": "Rapidly growing IT and automotive hub in the upper Mutha-Mula river basin. Complex radial road network (NH-48, Solapur Rd, Ahmednagar Rd) experiencing intense private two-wheeler and four-wheeler congestion, coupled with riverfront environmental sensitivity.",
        "key_landmarks": "Mutha Riverfront, BRTS Corridors, Hinjawadi / Kharadi corridors, Shivajinagar Junction",
    },
    "mumbai": {
        "authority": "Brihanmumbai Municipal Corporation (BMC)",
        "context": "India's financial capital characterized by a narrow coastal peninsular topography, high population density, and dependence on suburban railway spines (Western, Central, Harbour). Strict CRZ regulations, coastal reclamation constraints, and tidal flood risks.",
        "key_landmarks": "Eastern Freeway, Western Express Highway, Sanjay Gandhi National Park buffer, Mithi River",
    },
    "nagpur": {
        "authority": "Nagpur Municipal Corporation (NMC)",
        "context": "Geographic center of India ('Zero Mile') and prime multi-modal logistics hub in Vidarbha. Features the Nag river basin, high industrial freight traffic, and high summer heat stress requiring extensive urban shading and dust control.",
        "key_landmarks": "Zero Mile Stone, MIHAN SEZ, Ring Road Corridors, Ambazari Lake watershed",
    },
    "nashik": {
        "authority": "Nashik Municipal Corporation (NMC)",
        "context": "Major industrial and religious center on the banks of the Godavari river. Experiences seasonal pilgrimage spikes (Kumbh Mela infrastructure), rapid peripheral expansion along Ambad and Satpur MIDC zones, and significant agricultural transit.",
        "key_landmarks": "Godavari Riverfront, Gangapur Dam catchment, Ambad MIDC corridor, Mumbai-Agra Highway (NH-848)",
    },
    "chhatrapati sambhajinagar": {
        "authority": "Chhatrapati Sambhajinagar Municipal Corporation (CSMC)",
        "context": "Principal commercial and heritage center of Marathwada located in the semi-arid Kham river basin. Strong automobile and pharmaceutical manufacturing clusters (Waluj, Shendra) needing industrial effluent control and green buffer expansion.",
        "key_landmarks": "Kham River, Waluj MIDC, Shendra DMIC Node, Jalna Road Arterial",
    },
    "thane": {
        "authority": "Thane Municipal Corporation (TMC)",
        "context": "Dense urban local body in Mumbai Metropolitan Region bordered by Ulhas River creek and Sanjay Gandhi National Park. Severe transit bottlenecks along Ghodbunder Road and suburban interchange corridors.",
        "key_landmarks": "Ghodbunder Road corridor, Thane Creek Flamingo Sanctuary periphery, Parsik Hill slopes",
    },
    "pimpri-chinchwad": {
        "authority": "Pimpri-Chinchwad Municipal Corporation (PCMC)",
        "context": "One of Asia's largest automotive and industrial clusters in the Pavana river basin. Advanced municipal infrastructure with wide arterial roads, but high industrial air emissions and rapid labor migrant population influx.",
        "key_landmarks": "Pavana River corridor, Bhosari MIDC, Pune-Nashik Highway corridor, Thergaon industrial zone",
    },
    "solapur": {
        "authority": "Solapur Municipal Corporation (SMC)",
        "context": "Key textile and powerloom hub in southern Maharashtra situated on the drought-prone semi-arid Deccan plateau. Faces acute water scarcity, high ambient dust, and decentralized cotton waste processing challenges.",
        "key_landmarks": "Sambre Lake, MIDC Textile Park, Pune-Hyderabad Highway (NH-65), Siddheshwar Temple precinct",
    },
    "kolhapur": {
        "authority": "Kolhapur Municipal Corporation (KMC)",
        "context": "Historic agro-industrial and foundry hub on the banks of the Panchganga river. Subject to recurring monsoon floods, dense traditional core congestion, and agricultural processing waste discharges.",
        "key_landmarks": "Panchganga Riverfront, Rankala Lake basin, Shiroli / Gokul Shirgaon MIDC, Mahalaxmi Temple precinct",
    },
    "amravati": {
        "authority": "Amravati Municipal Corporation (AMC)",
        "context": "Premier educational and commercial center of western Vidarbha along the NH-53 (Mumbai-Kolkata) corridor. Requires systematic green space preservation and decentralized solid waste management for its expanding peripheral wards.",
        "key_landmarks": "Wadali Lake, Badnera Junction corridor, MIDC Amravati, Chhatri Talao",
    },
    "navi mumbai": {
        "authority": "Navi Mumbai Municipal Corporation (NMMC)",
        "context": "Planned modern twin-city with structured nodal sectors, Parsik Hill green buffer, and Thane-Belapur industrial belt. Priority focuses on coastal mangrove protection, EV bus infrastructure, and industrial air emissions monitoring.",
        "key_landmarks": "Palm Beach Road, Thane-Belapur MIDC, Parsik Hill Reserve, Belapur CBD",
    },
    "kalyan-dombivli": {
        "authority": "Kalyan-Dombivli Municipal Corporation (KDMC)",
        "context": "Major commuter railway junction in eastern MMR with exceptionally high passenger footfalls and dense suburban neighborhoods. Critical need for transit-oriented station area redevelopment and Ulhas river flood buffer management.",
        "key_landmarks": "Kalyan Railway Terminal precinct, Waldhuni River corridor, Dombivli MIDC Phase I & II",
    },
}

# Default context template for any tier-2/3 Maharashtra urban local body
DEFAULT_LOCAL_CONTEXT = {
    "authority": "{city} Municipal Authority",
    "context": "Key regional urban center in Maharashtra undergoing demographic and vehicular expansion. Balances municipal service delivery, local environmental preservation, and regional highway transit connectivity under State urban planning frameworks.",
    "key_landmarks": "Central Municipal Core, Regional Highway Corridor, Local Waterbody Catchment",
}

# Comprehensive indicator intervention blueprints
INDICATOR_BLUEPRINTS = {
    "Air Quality": {
        "title": "Road Dust Abatement, CAAQMS Expansion & Low-Emission Corridor Management",
        "objective": "Suppress ambient particulate concentrations (PM10 and PM2.5) to achieve National Clean Air Programme (NCAP) 20-30% reduction targets.",
        "phases": {
            "phase_1_immediate": "Months 0–6 (Immediate Operational Controls): Deploy mechanical street sweepers on primary transit corridors; mandate dust screens, tire-washing bays, and water misting at all construction sites >500 m²; conduct strict PUC enforcement blitzes at fuel outlets; enforce zero-tolerance night patrols against open biomass and municipal waste burning.",
            "phase_2_medium": "Months 6–18 (Infrastructure & Targeted Upgrades): Pave unpaved road shoulders and medians with permeable interlocking blocks; establish localized CAAQMS micro-monitoring stations at schools, hospitals, and major traffic intersections; mandate wet scrubbers on industrial boilers; transition municipal utility and garbage tipper fleets to CNG/EV.",
            "phase_3_long": "Months 18–36 (Systemic Policy & Green Transition): Implement Low Emission Zones (LEZ) in dense commercial market centers with restricted freight entry hours; expand electric bus fleets under PM e-Bus Sewa; plant 3-tier particulate-trapping shelterbelts along regional highway bypasses.",
        },
        "spatial_feasibility": {
            "strategy": "High-Dust Corridor Buffers & Monitoring Network Siting",
            "spatial_interventions": "Identify arterial corridors with heavy freight movements for continuous 15-meter vegetative noise and dust buffers using high-SLA native species (Azadirachta indica, Ficus religiosa, Pongamia pinnata). Site micro-monitoring units within 50 meters of sensitive educational and healthcare facilities.",
            "feasibility_parameters": "Minimum 2.0m unpaved verge paving; continuous green buffer width 10–15m along national/state highways; 500m buffer around stone crushers and ready-mix concrete plants.",
        },
        "policy_citations": [
            {
                "framework": "National Clean Air Programme (NCAP)",
                "authority": "Ministry of Environment, Forest and Climate Change (MoEFCC)",
                "clause": "Comprehensive City Action Plan for Non-Attainment Cities & 15th Finance Commission Air Quality Performance Benchmark.",
                "url": "https://moef.gov.in/en/division/environment-divisions/air-pollution/national-clean-air-programme-ncap/",
            },
            {
                "framework": "Graded Response Action Plan & CPCB Guidelines",
                "authority": "Central Pollution Control Board (CPCB) / MPCB",
                "clause": "Standard Operating Procedures for Dust Mitigation from Construction and Demolition Activities (2020).",
                "url": "https://cpcb.nic.in/",
            },
        ],
        "kpis": [
            "20–30% reduction in annual average PM10 and PM2.5 levels",
            ">90% coverage of mechanical sweeping on primary arterials",
            "Zero documented open burning incidents in municipal limits",
            "100% construction site compliance with dust mitigation norms",
        ],
        "funding": "15th Finance Commission Air Quality Grants for Million-Plus / Non-Attainment Cities, NCAP Performance Grants, and MoRTH Highway Greening Fund.",
    },

    "Waste Management": {
        "title": "100% Source Segregation, Decentralized Processing & Legacy Dumpsite Bioremediation",
        "objective": "Achieve complete segregation at generation, maximize scientific waste processing, and eliminate open dumping per Solid Waste Management Rules 2016.",
        "phases": {
            "phase_1_immediate": "Months 0–6 (Operational Enforcement & Route Rationalization): Enforce strict color-coded three-way source segregation (wet, dry, domestic hazardous) across all residential and commercial wards; install GPS tracking on 100% of primary collection tippers; eliminate open roadside garbage vats (dhalaos); levy spot fines for commercial mixed waste dumping.",
            "phase_2_medium": "Months 6–18 (Decentralized Processing & Informal Integration): Construct ward-level Materials Recovery Facilities (MRFs) with mechanical conveyor-sorters and baling machines; set up 5–10 TPD biomethanation plants at vegetable/fruit wholesale markets to generate bio-CNG/electricity; formally register and integrate informal waste-pickers into municipal collection cooperatives.",
            "phase_3_long": "Months 18–36 (Full Resource Recovery & Legacy Reclamation): Execute scientific biomining and capping of legacy waste dumpsites to reclaim valuable public land; partner with regional cement kilns for 100% Refuse Derived Fuel (RDF) off-take; operationalize an automated IoT weighbridge and processing facility dashboard.",
        },
        "spatial_feasibility": {
            "strategy": "Decentralized Ward Processing Hubs & Transit Transfer Optimization",
            "spatial_interventions": "Situate decentralized MRF centers within a 2.5–3.0 km catchment radius of residential wards to minimize haulage costs. Locate organic composting / biomethanation units adjacent to major agricultural produce markets (APMCs). Ensure minimum 500m scientific buffer between disposal sites and natural waterbodies.",
            "feasibility_parameters": "Minimum 500–1000 m² site area for ward MRF; 1000–2500 m² for decentralized 10 TPD biomethanation; mandatory leachate collection sump and effluent treatment connection.",
        },
        "policy_citations": [
            {
                "framework": "Solid Waste Management (SWM) Rules, 2016",
                "authority": "Ministry of Environment, Forest and Climate Change (MoEFCC)",
                "clause": "Rule 15: Duties of local authorities for door-to-door collection, segregated transport, decentralized composting, and phase-out of open dumping.",
                "url": "https://mpcb.gov.in/waste-management/municipal-solid-waste",
            },
            {
                "framework": "Swachh Bharat Mission (Urban) 2.0 Operational Guidelines",
                "authority": "Ministry of Housing and Urban Affairs (MoHUA)",
                "clause": "Remediation of all legacy dumpsites and complete processing of municipal wet and dry solid waste.",
                "url": "https://sbmurban.org/",
            },
        ],
        "kpis": [
            ">95% door-to-door collection with verified source segregation",
            ">85% municipal solid waste scientifically processed and diverted from landfills",
            "100% remediation and reclamation of legacy dumpsite land area",
            "Zero untreated leachate discharge into natural drainage nullahs",
        ],
        "funding": "Swachh Bharat Mission (Urban) 2.0, 15th Finance Commission Solid Waste Management Grants, and AMRUT 2.0 sanitation sub-mission.",
    },

    "Green Space": {
        "title": "Miyawaki Pocket Forests, Accessible Neighborhood Parks & Riparian Corridors",
        "objective": "Expand public per capita green space toward the URDPFI guideline of 10-12 m²/person and ensure equitable access within 500m of all residential areas.",
        "phases": {
            "phase_1_immediate": "Months 0–6 (GIS Cadastral Audit & Boundary Protection): Complete a comprehensive GIS cadastral mapping of all municipal reservations for gardens, playgrounds, and public open spaces; evict encroachments and erect boundary fencing; launch native tree plantation drives on unutilized government institution premises.",
            "phase_2_medium": "Months 6–18 (Pocket Park Development & Urban Afforestation): Establish dense Miyawaki micro-forests on vacant municipal plots (>0.2 hectare) using fast-growing native biodiversity; develop universally accessible neighborhood sensory parks within high-density residential wards lacking recreational facilities.",
            "phase_3_long": "Months 18–36 (Riparian Greenway & Master Plan Integration): Naturalize riverbanks, lakeshores, and natural nullah buffers into continuous pedestrian greenway corridors; enforce mandatory 15% open space reservation in all new commercial/residential layouts per Maharashtra Unified DCPR (UDCPR 2020); establish urban biodiversity conservation zones.",
        },
        "spatial_feasibility": {
            "strategy": "Vacant Parcel Afforestation & 500m Walking Catchment Optimization",
            "spatial_interventions": "Identify vacant municipal land parcels, utility rights-of-way, and canal embankments for pocket park conversion. Prioritize wards where satellite imagery shows green coverage <2% and distance to nearest public park exceeds 800 meters. Implement permeable walking paths, solar lighting, and native flora.",
            "feasibility_parameters": "Minimum 0.1 hectare for urban pocket park / Miyawaki forest; minimum 0.5–1.0 hectare for neighborhood park per URDPFI norms; maximum 500m walking radius (10-minute walk).",
        },
        "policy_citations": [
            {
                "framework": "Urban and Regional Development Plans Formulation and Implementation (URDPFI) Guidelines 2015",
                "authority": "Ministry of Housing and Urban Affairs (MoHUA)",
                "clause": "Open Space Norms: 10–12 m² per capita green and recreational open space in urban areas; neighborhood park within 500m walking radius.",
                "url": "https://mohua.gov.in/upload/uploadfiles/files/URDPFI_Guidelines_Vol_I.pdf",
            },
            {
                "framework": "Maharashtra Unified Development Control and Promotion Regulations (UDCPR 2020)",
                "authority": "Urban Development Department, Government of Maharashtra",
                "clause": "Regulation 3.4 & 3.5: Mandatory Open Space Reservation and Green Buffer alongside natural water streams and rivers.",
                "url": "https://dtp.maharashtra.gov.in/",
            },
        ],
        "kpis": [
            "Increase green cover towards state benchmark of >10% of municipal area",
            ">80% of urban residents living within a 10-minute walk (500m) of an accessible green space",
            "100% survival rate monitoring of native saplings via geo-tagged tree census",
            "Complete ecological restoration and vegetative buffering of local river/nullah banks",
        ],
        "funding": "AMRUT 2.0 Green Spaces and Parks Sub-Scheme, MoEFCC Nagar Van Yojana, and Smart Cities Mission Public Realm Upgrades.",
    },

    "Traffic": {
        "title": "Non-Motorized Transport (NMT) Corridors, Signal Optimization & Transit-Oriented Mobility",
        "objective": "Mitigate chronic intersection congestion, reduce private motor vehicle dependence, and provide safe pedestrian and public transit infrastructure.",
        "phases": {
            "phase_1_immediate": "Months 0–6 (Bottleneck Clearance & Traffic Management): Remove pedestrian footpath encroachments along key arterial roads; optimize signal cycle timings using Adaptive Traffic Control Systems (ATCS) at top congested junctions; enforce strict junction yellow-box rules and anti-jaywalking pedestrian refuge islands.",
            "phase_2_medium": "Months 6–18 (Active Mobility & Bus Priority Infrastructure): Construct continuous, universally accessible 2.5m wide pedestrian sidewalks and segregated cycle tracks on trunk routes; introduce high-frequency electric midi-bus feeder routes connecting railway/bus terminals to major employment nodes; implement paid on-street parking management.",
            "phase_3_long": "Months 18–36 (High-Capacity Transit & Integrated Multimodal Hubs): Implement dedicated bus priority lanes or Bus Rapid Transit System (BRTS) on major radial spines; construct multi-modal interchange hubs with park-and-ride facilities; integrate unified ticketing under the National Common Mobility Card (NCMC).",
        },
        "spatial_feasibility": {
            "strategy": "Complete Streets Cross-Section & Multimodal Junction Redesign",
            "spatial_interventions": "Reallocate road right-of-way (RoW) according to Complete Streets principles: allocate 35–45% of cross-section to non-motorized and public transit modes. Redesign high-crash intersections with tighter curb radii, high-visibility zebra crossings, and pedestrian bulb-outs.",
            "feasibility_parameters": "Minimum 2.0–2.5m clear sidewalk width; minimum 2.0m segregated one-way bicycle track; 30m minimum RoW for dedicated bus priority lane implementation.",
        },
        "policy_citations": [
            {
                "framework": "National Urban Transport Policy (NUTP 2014)",
                "authority": "Ministry of Housing and Urban Affairs (MoHUA)",
                "clause": "Priority allocation of road space to public transport and non-motorized modes; integration of land use and transport planning.",
                "url": "https://mohua.gov.in/cms/transport.php",
            },
            {
                "framework": "Indian Roads Congress (IRC) Guidelines for Urban Roads",
                "authority": "Indian Roads Congress (IRC:103-2012 / IRC:SP:107-2015)",
                "clause": "Guidelines for Pedestrian Facilities and Design of Urban Intersections for Safety and Capacity.",
                "url": "https://irc.nic.in/",
            },
        ],
        "kpis": [
            "20–30% increase in public transport modal share over 3 years",
            ">25% reduction in average peak-hour travel delay at major intersections",
            ">80% of arterial roads equipped with continuous, obstruction-free pedestrian footpaths",
            "Zero pedestrian and cyclist fatalities on designated Complete Streets corridors",
        ],
        "funding": "PM e-Bus Sewa Scheme, AMRUT 2.0 Urban Transport Component, State Urban Transport Fund, and Smart Cities Mission Traffic Command Centers.",
    },

    "Population Density": {
        "title": "Transit-Oriented Development (TOD), Ward Infrastructure Equalization & Balanced Growth",
        "objective": "Distribute urban demographic pressure, upgrade infrastructure carrying capacities in hyper-dense wards, and promote mixed-use transit corridors.",
        "phases": {
            "phase_1_immediate": "Months 0–6 (Ward Vulnerability & Service Audit): Conduct fine-grained ward-level infrastructure audits mapping water pressure, sewer drainage bottlenecks, fire access limitations, and health clinic access across high-density wards; enforce building safety setbacks and emergency egress routes.",
            "phase_2_medium": "Months 6–18 (Decentralized Amenities & Network Upgrades): Upgrade water distribution and underground sewerage capacities in high-density pockets to meet CPHEEO per capita service benchmarks; establish decentralized municipal service centers and urban primary health centers (UPHCs) within 15-minute walking catchments.",
            "phase_3_long": "Months 18–36 (TOD Zoning & Secondary Growth Nodes): Implement Transit-Oriented Development (TOD) zoning allowing higher Floor Space Index (FSI 3.0 to 4.0) within 500m of major transit corridors with mandatory inclusion of affordable housing; incentivize secondary growth centers on peripheral municipal land to de-densify the historical core.",
        },
        "spatial_feasibility": {
            "strategy": "TOD Station Area Delineation & Carrying Capacity Zoning",
            "spatial_interventions": "Delineate 500-meter Transit-Oriented Development influence zones along major transit corridors. Permit higher density and mixed-use commercial/residential development only on roads with minimum 24m Right-of-Way. Preserve open spaces and green buffers in high-density redevelopments.",
            "feasibility_parameters": "Minimum 24m road width for high-FSI (>3.0) incentives; mandatory 15% ground-level public open space reservation in clustered redevelopments; minimum 100% underground sewerage connectivity.",
        },
        "policy_citations": [
            {
                "framework": "National Transit Oriented Development (TOD) Policy 2017",
                "authority": "Ministry of Housing and Urban Affairs (MoHUA)",
                "clause": "High-density mixed-use development within walking distance of rapid transit stations; reduction of automobile dependency.",
                "url": "https://mohua.gov.in/upload/uploadfiles/files/Transit_Oriented_Development_Policy.pdf",
            },
            {
                "framework": "Maharashtra Unified DCPR (UDCPR 2020) - Chapter 10",
                "authority": "Urban Development Department, Government of Maharashtra",
                "clause": "Transit-Oriented Development Regulations and Special FSI Provisions for Mass Rapid Transit System Corridors.",
                "url": "https://dtp.maharashtra.gov.in/",
            },
        ],
        "kpis": [
            "100% piped drinking water and underground sewerage coverage across all dense wards",
            "100% of urban residents within 15-minute reach of primary healthcare and civic amenities",
            "Balanced Floor Space Index (FSI) utilization with mandatory public open space reservation",
            "Zero unserviced informal settlement pockets in municipal boundary",
        ],
        "funding": "Special Assistance to States for Capital Investment (Urban Reforms), Pradhan Mantri Awas Yojana (Urban) 2.0, and 15th Finance Commission Basic Urban Grants.",
    },
}


def _get_city_context(city_name: str) -> Dict[str, str]:
    """Retrieve localized administrative and geographical context for a Maharashtra city."""
    key = normalize_city_name(city_name)
    if key in CITY_LOCAL_CONTEXT:
        return CITY_LOCAL_CONTEXT[key]
    
    # Generic fallback with city name substitution
    return {
        "authority": DEFAULT_LOCAL_CONTEXT["authority"].format(city=city_name),
        "context": f"{city_name} is an important urban center in Maharashtra requiring balanced infrastructure expansion, environmental conservation, and proactive municipal service management.",
        "key_landmarks": f"Central {city_name} Municipal Core, Regional Transit Arterial",
    }


def generate_recommendations_for_city(
    city_name: str,
    city_score: Optional[Dict[str, Any]] = None,
    spatial_status: Optional[Dict[str, Any]] = None,
    include_rag: bool = True,
) -> List[Dict[str, Any]]:
    """
    Generate complete, valid, evidence-grounded recommendations for ALL indicators of a city.
    Recommendations are sorted by priority:
      1. Critical Problem Areas (Score < 40)
      2. Priority Upgrades / Needs Attention (40 <= Score < 60)
      3. Strategic Optimization / Maintenance (Score >= 60, or proxy metrics)
    Guarantees non-empty, actionable, localized recommendations for every Maharashtra city.
    """
    if city_score is None:
        city_score = get_city_score(city_name)

    city_context = _get_city_context(city_name)
    classifications = classify_indicators(city_score)
    spatial = spatial_status or get_spatial_readiness(city_name)

    # Classify priority order
    priority_order = {"Problem Area": 0, "Needs Attention": 1, "Acceptable": 2, "Unavailable": 3}
    sorted_items = sorted(
        classifications,
        key=lambda item: (priority_order.get(item["classification"], 4), (item["score"] if item["score"] is not None else 999))
    )

    recommendations = []
    for item in sorted_items:
        indicator_name = item["indicator"]
        blueprint = INDICATOR_BLUEPRINTS.get(indicator_name)
        if not blueprint:
            continue

        score = item["score"]
        classification = item["classification"]

        # Assign priority tier
        if classification == "Problem Area":
            priority_tier = "Critical (Immediate)"
        elif classification == "Needs Attention":
            priority_tier = "High Priority"
        else:
            priority_tier = "Strategic Optimization"

        # Construct localized diagnostic
        raw_val = item["raw_value"]
        unit = item["unit"]
        if raw_val is not None:
            diagnostic = f"{city_name} exhibits an observed {indicator_name.lower()} baseline of {raw_val} {unit} (normalized score: {score if score is not None else 'N/A'}/100, status: {classification})."
        else:
            diagnostic = f"{city_name} {indicator_name.lower()} is tracked as an urban pressure metric under municipal governance."

        executive_summary = (
            f"Under the jurisdiction of {city_context['authority']}, {diagnostic} "
            f"{blueprint['objective']} Spatial planning and phased capital interventions are tailored to {city_name}'s urban morphology."
        )

        rec_entry = {
            "indicator": indicator_name,
            "key": item["key"],
            "score": score,
            "raw_value": raw_val,
            "unit": unit,
            "classification": classification,
            "priority": priority_tier,
            "title": blueprint["title"],
            "action": blueprint["phases"]["phase_1_immediate"],
            "executive_summary": executive_summary,
            "local_authority": city_context["authority"],
            "local_context": city_context["context"],
            "key_landmarks": city_context.get("key_landmarks", ""),
            "phased_roadmap": blueprint["phases"],
            "spatial_feasibility": blueprint["spatial_feasibility"],
            "policy_citations": blueprint["policy_citations"],
            "target_kpis": blueprint["kpis"],
            "funding_mechanisms": blueprint["funding"],
            "recommendation_type": "rag_grounded_decision_support",
            "evidence_status": "not_retrieved",
            "evidence": [],
            "generated_text": None,
            "feasibility": "actionable_local_plan",
            "spatial_message": spatial.get("message", "Spatial parameters defined per URDPFI / UDCPR norms."),
        }

        # Retrieve RAG evidence from local FAISS index
        if include_rag:
            try:
                from .rag_service import get_recommendation_evidence
                grounded = get_recommendation_evidence(item, spatial)
                rec_entry.update({
                    "evidence_status": grounded["evidence_status"],
                    "evidence": grounded["evidence"],
                    "generation_status": grounded["generation"]["status"],
                    "generated_text": grounded["generation"]["text"],
                    "generation_message": grounded["generation"]["message"],
                    "recommendation_type": "retrieval_augmented" if grounded["generation"]["text"] else "rag_grounded_decision_support",
                })
            except Exception:
                pass

        recommendations.append(rec_entry)

    return recommendations


def generate_recommendations(
    problem_areas: List[Dict[str, Any]],
    spatial_status: Optional[Dict[str, Any]] = None,
    include_rag: bool = False,
    city_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Backwards-compatible interface. If problem_areas is provided and non-empty,
    returns rich recommendations for those problem areas. If problem_areas is empty
    and a city_name is available, generates the full recommendation suite so it is NEVER empty.
    """
    # If city_name is provided or can be inferred
    if not problem_areas and city_name:
        return generate_recommendations_for_city(city_name, spatial_status=spatial_status, include_rag=include_rag)

    # If problem_areas were provided directly
    results = []
    for area in problem_areas:
        indicator_name = area["indicator"]
        blueprint = INDICATOR_BLUEPRINTS.get(indicator_name)
        score = area.get("score")
        classification = area.get("classification", "Problem Area")

        if blueprint:
            title = blueprint["title"]
            action = blueprint["phases"]["phase_1_immediate"]
            evidence_note = f"Grounded in {blueprint['policy_citations'][0]['framework']} and URDPFI 2015 urban planning norms."
            phases = blueprint["phases"]
            spatial_rec = blueprint["spatial_feasibility"]
            citations = blueprint["policy_citations"]
            kpis = blueprint["kpis"]
            funding = blueprint["funding"]
        else:
            title = f"Intervene in {indicator_name}"
            action = f"Implement targeted upgrades and regulatory monitoring for {indicator_name}."
            evidence_note = "Review observed indicators and state planning guidelines before implementation."
            phases = {"phase_1_immediate": action, "phase_2_medium": action, "phase_3_long": action}
            spatial_rec = {"strategy": "General zoning review", "spatial_interventions": "Assess local ward needs", "feasibility_parameters": "Standard urban norms"}
            citations = []
            kpis = ["Improve indicator score by 15-20%"]
            funding = "State Urban Development Fund"

        rec = {
            **area,
            "title": title,
            "action": action,
            "evidence_note": evidence_note,
            "priority": "Critical (Immediate)" if classification == "Problem Area" else "High Priority",
            "phased_roadmap": phases,
            "spatial_feasibility": spatial_rec,
            "policy_citations": citations,
            "target_kpis": kpis,
            "funding_mechanisms": funding,
            "recommendation_type": "rag_grounded_decision_support",
            "evidence_status": "not_retrieved",
            "evidence": [],
            "generated_text": None,
            "feasibility": "actionable_local_plan",
            "spatial_message": (spatial_status or {}).get("message", "Spatial parameters defined per URDPFI / UDCPR norms."),
        }

        if include_rag:
            try:
                from .rag_service import get_recommendation_evidence
                grounded = get_recommendation_evidence(area, spatial_status)
                rec.update({
                    "evidence_status": grounded["evidence_status"],
                    "evidence": grounded["evidence"],
                    "generation_status": grounded["generation"]["status"],
                    "generated_text": grounded["generation"]["text"],
                    "generation_message": grounded["generation"]["message"],
                    "recommendation_type": "retrieval_augmented" if grounded["generation"]["text"] else "rag_grounded_decision_support",
                })
            except Exception:
                pass

        results.append(rec)

    return results
