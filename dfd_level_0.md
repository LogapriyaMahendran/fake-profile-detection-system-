# Data Flow Diagram (DFD) - Level 0

The DFD Level 0 (Context Diagram) defines the high-level boundary interface, showing the information flows between the central system process and the external entities.

```mermaid
graph LR
    User([User Entity])
    Admin([Admin Entity])
    
    subgraph Boundary["System Processing Boundary"]
        System((Fake Profile Detection Process 0.0))
    end
    
    %% User flows
    User -->|User Credentials| System
    User -->|Target Profile Metrics| System
    System -->|Prediction Results & Explanation| User
    System -->|Filtered Log Reports CSV/JSON| User
    
    %% Admin flows
    Admin -->|Admin Access Credentials| System
    Admin -->|Dataset Training CSV| System
    System -->|System Analytics Charts| Admin
    System -->|Login Logs & Training Status| Admin
```
