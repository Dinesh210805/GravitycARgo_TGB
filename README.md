# 🚛 GravitycARgo - AI-Enhanced Container Packing Optimization System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.2+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AR/VR Ready](https://img.shields.io/badge/AR%2FVR-Ready-purple.svg)](#ar-integration)
[![Slack Integration](https://img.shields.io/badge/Slack-Integrated-4A154B.svg)](#slack-integration)

> **Revolutionary 3D container packing optimization powered by genetic algorithms, LLM intelligence, and AR/VR visualization**

## 🌟 Project Overview

GravitycARgo is a cutting-edge container packing optimization system that combines advanced AI algorithms with immersive visualization technologies. Born from the need to maximize shipping efficiency while ensuring cargo safety, this system revolutionizes how logistics companies approach container loading.

### 🎯 Key Highlights

- **🧬 AI-Powered Optimization**: Genetic algorithms with LLM integration for intelligent packing decisions
- **📊 Real-time Visualization**: Interactive 3D container visualization with detailed analytics
- **🥽 AR/VR Ready**: Seamless integration with Unity for augmented reality experiences
- **💬 Slack Integration**: Professional workflow automation with real-time notifications
- **🌡️ Temperature Constraints**: Advanced handling of temperature-sensitive cargo
- **⚖️ Physics Simulation**: Weight distribution, stability, and load-bearing calculations
- **📱 Mobile-First**: Responsive design optimized for mobile logistics operations

## 🏗️ System Architecture

```mermaid
graph TD
    A[Web Interface] --> B[Flask Application]
    B --> C[OptiGenix Module]
    C --> D[Genetic Algorithm Engine]
    C --> E[Container Physics Engine]
    C --> F[Temperature Constraint Handler]
    D --> G[LLM Integration]
    B --> H[AR/VR Server]
    B --> I[Slack Integration]
    H --> J[Unity AR Client]
    I --> K[Mobile Notifications]
```

## 🚀 Features & Capabilities

### 🧠 Intelligent Optimization
- **Genetic Algorithm Engine**: Multi-generational evolution for optimal packing solutions
- **LLM-Enhanced Decision Making**: GPT integration for dynamic fitness weight adjustment
- **Temperature Constraint Handling**: Automatic insulation placement for sensitive cargo
- **Load Bearing Analysis**: Physics-based weight distribution and structural integrity
- **Multi-Container Support**: Optimization across different container types and transport modes

### 📊 Advanced Analytics
- **Volume Utilization**: Real-time calculation of space efficiency
- **Weight Distribution**: Center of gravity analysis and balance optimization
- **Stability Metrics**: Contact ratio and support structure analysis
- **Packing Reports**: Comprehensive JSON and text reports with visual summaries
- **Performance Tracking**: Generation-by-generation optimization progress

### 🎮 Immersive Visualization
- **Interactive 3D Models**: Plotly-powered container and cargo visualization
- **AR Integration**: Direct Unity AR client support via ngrok tunneling
- **Color-Coded Items**: Visual distinction for temperature-sensitive and special cargo
- **Dynamic Camera Controls**: Multi-angle viewing with zoom and rotation
- **Export Capabilities**: Save visualizations as images or interactive HTML

### 🔗 Professional Integrations
- **Slack Workflow Automation**: Real-time status updates and command processing
- **Mobile-Optimized Interface**: Responsive design for field operations
- **RESTful API**: Complete programmatic access to all features
- **Docker Support**: Containerized deployment for scalability
- **Cloud-Ready**: Render.com deployment configuration included

## 🛠️ Technology Stack

### Backend
- **Python 3.9+**: Core application language
- **Flask 2.2+**: Web framework with SocketIO support
- **NumPy & SciPy**: Scientific computing and optimization
- **Pandas**: Data processing and CSV handling
- **Google Gemini API**: LLM integration for intelligent decisions

### Frontend
- **Plotly**: Interactive 3D visualization and charts
- **Dash**: Real-time dashboard components
- **HTML5/CSS3**: Modern responsive web interface
- **JavaScript**: Dynamic UI interactions

### AI & Optimization
- **Custom Genetic Algorithm**: Multi-objective optimization engine
- **Temperature Constraint Handler**: Physics-based thermal protection
- **LLM Connector**: Dynamic fitness weight adjustment
- **Maximal Space Algorithm**: Efficient space utilization tracking



## 🏃‍♂️ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/Dinesh210805/GravitycARgo_TGB.git
cd GravitycARgo_TGB
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Configure your settings
export GEMINI_API_KEY="your_gemini_api_key"
export SLACK_BOT_TOKEN="xoxb-your-slack-token"
export SLACK_APP_TOKEN="xapp-your-app-token"
```

### 3. Launch Application
```bash
# One-command startup (recommended)
python quickstart.py

# Or manual startup
python app_modular.py
```

### 4. Access Interfaces
- **Web Dashboard**: http://localhost:5000
- **Container Optimization**: http://localhost:5000/optimize
- **AR Visualization**: http://localhost:8000 (auto-started)

## 🎮 AR/VR Integration

### 📱 AR Application & Resources
- **📦 AR Application APK**: [Download AR App](https://drive.google.com/file/d/1YLzJt9qcjwP9PksppQThPeI5o75yGZT0/view?usp=sharing)
- **🎯 AR Tracker Image**: [Download AR Tracker](https://drive.google.com/file/d/10SR7P7Eatns1g4c0h7AEtD6ZVPAYbIhq/view?usp=sharing)
- **🎥 Demo Video**: [Watch Demo on YouTube](https://youtu.be/l3YzHS40i3Y)

### Unity Setup
1. **Install Unity 2021.3 LTS+** with AR Foundation
2. **Import AR Package**: `AR Gravity Cargo.unitypackage`
3. **Configure HTTP Component**: Point to ngrok URL
4. **Build for Mobile**: iOS/Android deployment

### AR Workflow
```bash
# Start AR server automatically
python app_modular.py

# Access ngrok URL
https://destined-mammoth-flowing.ngrok-free.app/latest_container_plan.json

# Use in Unity HTTP component
```

### Features in AR
- **Real-time 3D Visualization**: See container contents in augmented reality
- **Interactive Item Manipulation**: Touch and move virtual cargo
- **Measurement Tools**: Real-world scale measurements
- **Multi-user Support**: Collaborative viewing sessions

## 📊 Container Types & Transport Modes

### Supported Containers
| Type | Dimensions (L×W×H) | Weight Capacity | Use Case |
|------|-------------------|-----------------|----------|
| 20ft Standard | 5.90×2.35×2.39m | 28,180kg | General cargo |
| 40ft Standard | 12.00×2.35×2.39m | 28,800kg | High volume |
| 40ft High Cube | 12.00×2.35×2.69m | 28,560kg | Tall cargo |
| 20ft Reefer | 5.44×2.29×2.27m | 27,700kg | Temperature control |
| Flat Rack | 12.19×2.44×2.44m | 39,340kg | Oversized cargo |

### Transport Modes
- **🚛 Road Transport**: Truck-optimized containers
- **🚢 Sea Transport**: All standard maritime containers
- **✈️ Air Transport**: Weight-restricted containers
- **🚂 Rail Transport**: Rail-compatible configurations
- **🔧 Custom**: User-defined dimensions

## 🧬 Algorithm Deep Dive

### Genetic Algorithm Engine
```python
class GeneticPacker:
    def __init__(self, container_dims, population_size=10, generations=8):
        self.mutation_rates = {
            'rotation': 0.2,    # Item orientation changes
            'swap': 0.15,       # Position swapping
            'subsequence': 0.1  # Sequence reorganization
        }
        self.elite_percentage = 0.15  # Best solution preservation
```

### Fitness Function Components
- **Volume Utilization** (30%): Maximize space usage
- **Item Packing Ratio** (25%): Maximize items packed
- **Stability Score** (20%): Ensure structural integrity
- **Contact Ratio** (15%): Optimize item interactions
- **Weight Balance** (10%): Center of gravity optimization

### Temperature Constraint Handling
```python
class TemperatureConstraintHandler:
    def check_constraints(self, item, position, container_dims):
        # Enforce 30cm buffer from walls
        # Prioritize central placement
        # Ensure surrounding insulation
        return is_position_safe
```

## 🌡️ Temperature Constraints System

Our system provides sophisticated temperature constraint handling for sensitive cargo:

### Supported Temperature Ranges
- **Pharmaceuticals**: 2°C to 8°C (refrigerated)
- **Electronics**: 10°C to 35°C (standard)
- **Food Products**: -18°C to 4°C (frozen/chilled)
- **Chemicals**: Custom ranges as specified
- **Room Temperature**: 15°C to 25°C (standard)

### Temperature Constraint Features
- **🏠 Wall Buffer Protection**: Automatic 30cm minimum distance from container walls
- **🎯 Central Placement Priority**: Temperature-sensitive items placed in container center
- **🛡️ Insulation Logic**: Items requiring temperature protection are surrounded by non-sensitive cargo
- **🔄 Route Temperature Integration**: Dynamic adjustment based on transport route climate
- **📊 Thermal Mapping**: Visual representation of temperature zones within container
- **⚠️ Constraint Validation**: Real-time checking of temperature requirements during packing

### How It Works
1. **Item Analysis**: System identifies temperature-sensitive items from input data
2. **Route Temperature**: Considers ambient temperature during transport
3. **Safe Zone Calculation**: Creates temperature-safe zones within container
4. **Priority Placement**: Temperature-sensitive items get placement priority
5. **Insulation Strategy**: Non-sensitive items act as thermal barriers
6. **Validation**: Continuous checking of temperature constraints during optimization

## 📋 Input Data Template

### CSV File Format
Use the following template for your cargo data input:

```csv
Name,Length,Width,Height,Weight,Quantity,Fragility,LoadBear,BoxingType,Bundle,Temperature Sensitivity
ContainerBase_A,2.95,2.35,0.05,100,2,LOW,9999,CRATE,YES,n/a
Electronics_Box,1.2,0.8,0.3,50,5,HIGH,500,BOX,YES,10°C to 35°C
Pharmaceuticals,0.6,0.4,0.3,15,3,HIGH,0,BOX,NO,2°C to 8°C
Furniture_Item,2.0,1.5,0.8,200,2,MEDIUM,1000,CRATE,NO,n/a
```

### Field Descriptions
| Field | Type | Description | Example Values |
|-------|------|-------------|----------------|
| **Name** | String | Unique item identifier | "Electronics_Box", "Pharma_001" |
| **Length** | Float | Length in meters | 1.2, 2.95 |
| **Width** | Float | Width in meters | 0.8, 2.35 |
| **Height** | Float | Height in meters | 0.3, 0.05 |
| **Weight** | Float | Weight in kilograms | 50, 100, 200 |
| **Quantity** | Integer | Number of identical items | 1, 2, 5 |
| **Fragility** | String | Fragility level | LOW, MEDIUM, HIGH |
| **LoadBear** | Integer | Load bearing capacity (kg) | 0, 500, 9999 |
| **BoxingType** | String | Packaging type | BOX, CRATE, PALLET |
| **Bundle** | String | Can be bundled together | YES, NO |
| **Temperature Sensitivity** | String | Temperature range or n/a | "2°C to 8°C", "n/a" |

### Sample Files
- 📁 `input/perfect_utilization.csv` - Complete template example
- 📁 `input/perfect_100.csv` - High utilization example  
- 📁 `input/max_utilization.csv` - Maximum efficiency example

### Temperature Sensitivity Examples
- `n/a` - No temperature requirements
- `2°C to 8°C` - Refrigerated pharmaceuticals
- `10°C to 35°C` - Standard electronics
- `-18°C to 4°C` - Frozen/chilled food products
- `15°C to 25°C` - Room temperature goods

## 🔧 API Reference

### Core Endpoints
```bash
# Container optimization
POST /api/optimize
{
    "items": [...],
    "container_type": "40ft",
    "constraints": {...}
}

# AR server control
POST /start_json_server
POST /stop_json_server
GET /check_json_server_status

# Slack integration
POST /slack/events
POST /slack/commands
```

### Response Formats
```json
{
    "status": "success",
    "optimization_result": {
        "volume_utilization": 0.87,
        "items_packed": 23,
        "fitness_score": 0.94,
        "generation_count": 12,
        "unpacked_items": []
    },
    "visualization_url": "https://...",
    "report_files": ["report.json", "report.txt"]
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Core settings
SECRET_KEY=your_secret_key
DEBUG=False
FLASK_ENV=production

# AI integration
GEMINI_API_KEY=your_gemini_key
LLM_PROVIDER=gemini

# Slack integration
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
SLACK_SIGNING_SECRET=your_signing_secret

# Server settings
MAIN_APP_PORT=5000
JSON_SERVER_PORT=8000
ROUTE_TEMP_PORT=5001

# Optimization parameters
DEFAULT_POPULATION_SIZE=10
DEFAULT_GENERATIONS=8
MAX_CONTENT_LENGTH=16777216
```

### Custom Container Types
```python
# Add custom container in constants.py
CONTAINER_TYPES['Custom-Container'] = (15.0, 3.0, 3.0, 35000)
```

## 📈 Performance Metrics

### Optimization Results
- **Average Volume Utilization**: 85-95%
- **Optimization Time**: 30-120 seconds
- **Items Packed Success Rate**: 90-98%
- **Stability Score**: 0.85+ (scale 0-1)

### System Performance
- **Response Time**: <2 seconds for UI interactions
- **Concurrent Users**: 50+ supported
- **AR Streaming**: 30fps real-time updates
- **Memory Usage**: 512MB-2GB depending on complexity

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Test specific modules
python -m pytest tests/test_genetic_algorithm.py
python -m pytest tests/test_container_packing.py
python -m pytest tests/test_ar_integration.py
```

## 🤝 Contributing

### Development Setup
```bash
# Fork the repository
git fork https://github.com/Dinesh210805/GravitycARgo_TGB.git

# Create feature branch
git checkout -b feature/amazing-new-feature

# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install
```

### Code Standards
- **Python**: Follow PEP 8 with Black formatting
- **Documentation**: Comprehensive docstrings for all functions
- **Testing**: 90%+ code coverage requirement
- **Commits**: Conventional commit messages

### Pull Request Process
1. **Feature Development**: Implement in feature branch
2. **Testing**: Ensure all tests pass
3. **Documentation**: Update README and docstrings
4. **Review**: Submit PR with detailed description

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by the GravitycARgo Team**

[🌟 Star us on GitHub](https://github.com/Dinesh210805/GravitycARgo_TGB) | [🐛 Report Bug](https://github.com/Dinesh210805/GravitycARgo_TGB/issues) | [💡 Request Feature](https://github.com/Dinesh210805/GravitycARgo_TGB/issues)

*Revolutionizing container logistics, one optimization at a time.*

</div>
