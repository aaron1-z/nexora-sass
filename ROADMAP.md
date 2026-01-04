# Nexora Engine Roadmap

## Sprint 1: Ingestion & Normalization
- [ ] Implement Ingestion Service (RSS, Web, API)
- [ ] Build Normalization Service (Deduplication, Cleaning)
- [ ] Set up Redis and PostgreSQL
- [ ] Deploy basic Docker Compose stack

## Sprint 2: Embeddings & Vector Memory
- [ ] Integrate OpenAI/Local Embeddings
- [ ] Set up Milvus/FAISS
- [ ] Implement VectorStore wrapper
- [ ] Ingest initial dataset and verify retrieval

## Sprint 3: Reasoning & Verification
- [ ] Build Reasoner Module (RAG pipeline)
- [ ] Implement Verifier (NLI/Self-consistency)
- [ ] Connect Reasoner to VectorStore
- [ ] Create basic evaluation set

## Sprint 4: Explainability & Scenarios
- [ ] Implement Provenance Mapper
- [ ] Build Scenario Tree Generator
- [ ] Develop Chain-of-Thought internal representation
- [ ] Integrate Explainability into API responses

## Sprint 5: Frontend & API Integration
- [ ] Build Next.js Dashboard
- [ ] Connect Frontend to API Gateway
- [ ] Implement Briefs and Scenarios UI
- [ ] Add real-time updates

## Sprint 6: Enterprise Hardening & Analytics
- [ ] Implement RBAC and SSO
- [ ] Set up Audit Logging
- [ ] Deploy Analytics Service
- [ ] Finalize Documentation and CI/CD pipelines
