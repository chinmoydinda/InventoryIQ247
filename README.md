<div align="center">

# 📦 InventoryIQ247

**The Open-Source Core & Early-Stage Hosted Developer Platform for Real-Time Inventory**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Java](https://img.shields.io/badge/Java-21%2B-orange.svg)](https://openjdk.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.4-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Cloud Preview](https://img.shields.io/badge/Cloud%20Platform-Early%20Developer%20Beta-6366f1.svg)](#hosted-developer-platform)
[![API](https://img.shields.io/badge/API-REST%20%7C%20Webhooks%20%7C%20OpenAPI-blueviolet.svg)](#api--developer-experience)

*Eliminate inventory race conditions, automate multi-SKU bundle assemblies, and sync stock across all channels 24/7. Self-host the engine or deploy via our early-stage hosted developer cloud.*

[Explore Hosted Cloud](#hosted-developer-platform) • [View Landing Page (docs/index.html)](file:///Users/chinmoy/Development/Projects/InventoryIQ247/docs/index.html) • [Quickstart](#quickstart) • [Architecture](#platform-architecture) • [Roadmap](#cloud-roadmap)

</div>

---

## 🌟 Why InventoryIQ247?

Building inventory infrastructure in-house is deceptive: what begins as simple table counts quickly spirals into deadlocks during flash sales, oversold out-of-stock items, broken bundle kits, and disconnected warehouse silos. Legacy monolithic ERPs (SAP, NetSuite) are slow, rigid, and painful for developers to integrate.

**InventoryIQ247** bridges this gap as a **developer-first inventory platform**:
- **Atomic Concurrency:** Strict row-level isolation and atomic reservations prevent double-allocation and overselling during peak traffic.
- **Dynamic Bundle & BOM Resolution:** Real-time stock computation for kits, assemblies, and multi-component products.
- **24/7 Event-Driven Sync:** Instant webhook dispatches, stock delta events, and transactional audit trails for e-commerce, POS, and WMS.
- **Dual-Plane Architecture:** Start completely free on our open-source embedded engine (Spring Boot + H2/PostgreSQL), then scale seamlessly to our **Hosted Developer Cloud** without changing your code.

---

## 🚀 Hosted Developer Platform (Early Access)

We are launching the **InventoryIQ247 Hosted Cloud**—an early-stage managed developer platform that removes the operational overhead of running inventory backends.

| Capability | Open-Source Core (Self-Hosted) | InventoryIQ247 Hosted Cloud (Beta) |
| :--- | :---: | :---: |
| **Hosting & Ops** | Self-managed (Local / VPS / Docker) | **Serverless Zero-Ops Cloud** |
| **Database** | Embedded H2 / Local PostgreSQL | **Distributed Managed Cloud PostgreSQL** |
| **API Endpoints** | Local REST Engine | **Global Edge Anycast Endpoints (<30ms)** |
| **Webhooks & Events** | Polling / Local Event Bus | **24/7 Managed Webhook Delivery with Auto-Retry** |
| **Authentication & RBAC** | Custom / Embedded App Auth | **Team Workspaces, API Key Rotation, OAuth2** |
| **Audit Trails** | Database Table Log | **Immutable Tamper-Evident Ledger + S3 Archival** |
| **Admin Console** | Embedded JavaFX GUI & Local Endpoints | **Cloud Developer Dashboard & Metrics Telemetry** |
| **Cost** | 100% Free & Open Source | **Free Developer Tier during Beta** |

> 💡 **Early Developer Cloud Access:** Visit our single-page landing page in [`docs/index.html`](file:///Users/chinmoy/Development/Projects/InventoryIQ247/docs/index.html) to request early API keys and join the waitlist.

---

## 🏛 Platform Architecture

```
                       ┌────────────────────────────────────────┐
                       │          E-Commerce / POS / WMS        │
                       │   (Shopify, Stripe, Custom Backends)   │
                       └───────────────────┬────────────────────┘
                                           │  REST / Webhooks
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                INVENTORYIQ247                                    │
│                                                                                  │
│   ┌─────────────────────────┐              ┌─────────────────────────────────┐   │
│   │   Hosted Cloud Platform │              │    Open Source Engine (Local)   │   │
│   │   - Global Edge Gateway │              │    - Spring Boot 3.2.4 (Java 21)│   │
│   │   - Multi-tenant Auth   │              │    - Spring Data JPA            │   │
│   │   - Managed Webhooks    │              │    - Lightweight H2 File DB     │   │
│   │   - Telemetry & Metrics │              │    - Embedded Desktop GUI (FX)  │   │
│   └────────────┬────────────┘              └────────────────┬────────────────┘   │
│                │                                            │                    │
│                └─────────────────────┬──────────────────────┘                    │
│                                      ▼                                           │
│                 ┌─────────────────────────────────────────┐                      │
│                 │      Core Inventory Execution Engine    │                      │
│                 │  • Atomic Stock Reservations & Locks    │                      │
│                 │  • Bundle / BOM Dynamic Calculation     │                      │
│                 │  • Excel / CSV Streaming Ingestion      │                      │
│                 │  • Immutable Movement Audit Log         │                      │
│                 └─────────────────────────────────────────┘                      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Developer Experience & API Preview

### 1. Atomic Stock Decrement / Movement
```bash
curl -X POST https://api.inventoryiq247.io/v1/stock/movements \
  -H "Authorization: Bearer iiq_live_98f4b107c" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "SKU-PRO-AUDIO-01",
    "quantity": 2,
    "type": "OUT",
    "reference": "ORDER-98231",
    "reason": "Fulfilled via Shopify Storefront"
  }'
```

### 2. Real-Time Dynamic Bundle Resolution
Bundles compute availability in real time based on component ratios without maintaining redundant stock states:
```json
{
  "bundleSku": "KIT-STREAMER-DELUXE",
  "availableQuantity": 14,
  "limitingComponent": {
    "sku": "SKU-MIC-STAND-DESK",
    "currentStock": 14,
    "requiredPerBundle": 1
  },
  "components": [
    { "sku": "SKU-MIC-CARDIOID", "required": 1, "stock": 45 },
    { "sku": "SKU-MIC-STAND-DESK", "required": 1, "stock": 14 },
    { "sku": "SKU-CABLE-XLR-3M", "required": 2, "stock": 60 }
  ]
}
```

### 3. Webhook Event Stream (24/7 Real-Time)
Receive immediate signals on inventory health:
```json
{
  "event": "inventory.threshold.low_stock",
  "timestamp": "2026-10-11T12:00:00Z",
  "data": {
    "sku": "SKU-MIC-STAND-DESK",
    "currentQuantity": 14,
    "reorderPoint": 20,
    "suggestedRestock": 50
  }
}
```

---

## 🛠 Quickstart (Open Source Core)

### Prerequisites
- **JDK 21+**
- **Maven 3.8+**

### Clone & Build
```bash
git clone https://github.com/inventoryiq/InventoryIQ247.git
cd InventoryIQ247
mvn clean package -DskipTests
```

### Run the Desktop Client & Local Engine
```bash
mvn javafx:run
```
Or launch the Spring Boot core:
```bash
mvn spring-boot:run
```
The local engine initializes an embedded, zero-configuration H2 database at `~/.stockmanager/data/inventory_db`.

---

## 🌐 Single-Page Landing Page

We provide a production-ready, dark-mode single-page landing page located at:
📁 [`docs/index.html`](file:///Users/chinmoy/Development/Projects/InventoryIQ247/docs/index.html)

### Features included in `docs/index.html`:
- ⚡️ Modern developer-first aesthetic (Supabase/Vercel styling, glassmorphism, accent glow).
- 🎮 **Live Interactive Inventory Sandbox:** Test atomic reservations and live bundle calculation in-browser.
- 🧪 **Multi-Language Code Tabs:** Instant cURL, Node.js, Python, and Java examples.
- 🔑 **Interactive Hosted Cloud Waitlist & API Key Generator:** Developers can enter their email and instantly generate a preview API key token.
- 📊 **Architecture & Comparison Matrix:** Highlights the strengths of InventoryIQ247 vs legacy ERPs and building from scratch.
- 📱 Fully responsive layout across mobile, tablet, and desktop screens.

To preview the landing page locally:
```bash
# Open directly in browser
open docs/index.html

# Or serve via Python:
cd docs && python3 -m http.server 3000
```

---

## 🗺 Cloud Roadmap

- [x] **Core Engine:** Spring Boot 3 + Java 21 JPA inventory primitives with optimistic locking.
- [x] **Dynamic Bundles:** BOM component resolution without stock divergence.
- [x] **Bulk Ingestion:** Streaming Apache POI Excel/CSV stock importer.
- [ ] **Phase 1 (Q4 2026):** Public Developer Cloud Beta (Multi-tenant PostgreSQL + Edge Gateway).
- [ ] **Phase 2 (Q1 2027):** 24/7 Outbound Webhooks with automatic retry & DLQ.
- [ ] **Phase 3 (Q2 2027):** Official SDKs for TypeScript, Python, and Go.
- [ ] **Phase 4 (Q3 2027):** Native Shopify, Amazon, and ERP connectors.

---

## 📄 License & Community

InventoryIQ247 core is licensed under the [Apache License 2.0](LICENSE).  
For enterprise inquiries and hosted cloud support, contact the team or star our repository!
