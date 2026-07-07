# Architecture Design

**Status:** Draft | Current
**Date:** [YYYY-MM-DD]

## 1. System Context

[What system or subsystem does this describe? What is its boundary? What external systems does it interact with?]

## 2. Design Goals

- **[Goal 1]:** [explanation]
- **[Goal 2]:** [explanation]

## 3. Component Architecture

```
+------------------+       +------------------+
|  Component A     |<----->|  Component B     |
|  Responsibility:  |       |  Responsibility:  |
|  ...              |       |  ...              |
+------------------+       +------------------+
        |                           |
        v                           v
+------------------+       +------------------+
|  Component C     |       |  Component D     |
+------------------+       +------------------+
```

### Component Descriptions

#### [Component A]
- **Responsibility:** [what this component does]
- **Owns:** [data, state, or resources it owns]
- **Depends on:** [other components or external services]
- **Interface:** [key entry points / API surface]

## 4. Data Flow

### Primary Flow
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Secondary Flows
- [Error flow description]
- [Edge case flow description]

### Data Model
- **[Entity]:** [description, key fields]
- **[Entity]:** [description, key fields]

## 5. Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| [Component A] | [tech] | [why chosen] |
| [Component B] | [tech] | [why chosen] |

## 6. Key Design Properties

- **[Property]:** [how it's achieved]
- **[Property]:** [how it's achieved]

## 7. Security & Reliability

- **Authentication:** [approach]
- **Authorization:** [approach]
- **Error handling:** [approach]
- **Data integrity:** [approach]
- **Observability:** [logging, metrics, alerting]

## 8. Open Questions

- [Question 1]
- [Question 2]

## 9. Assumptions

- [Assumption 1]
- [Assumption 2]

## Related Documents

- [Link to PRD]
- [Link to ADR-NNNN]
