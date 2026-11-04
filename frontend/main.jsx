import React, { useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { ArrowDown, ArrowRight, ArrowUp, BadgeCheck, BookOpen, Check, ChevronDown, FileText, FileUp, Gavel, Landmark, LoaderCircle, MessageSquareText, Plus, Scale, ShieldCheck, Sparkles, Upload, X } from 'lucide-react'
import './styles.css'

const suggestions = [
  { icon: Landmark, text: 'What are the termination conditions?' },
  { icon: BookOpen, text: 'How much notice is required to resign?' },
  { icon: ShieldCheck, text: 'Summarize the confidentiality clause' },
]

async function api(path, options = {}) {
  let response
  try {
    response = await fetch(path, options)
  } catch {
    throw new Error('Can’t reach the LegalLens API. In another terminal, install the Python requirements and start it with: python -m uvicorn app:app --reload')
  }
  const raw = await response.text()
  let body = {}
  try { body = raw ? JSON.parse(raw) : {} } catch { body = {} }
  if (!response.ok) throw new Error(body.detail || `The API returned an error (${response.status}). ${raw.slice(0, 180)}`)
  if (!body || typeof body !== 'object') throw new Error('The API returned an invalid response. Restart the backend and try again.')
  return body
}

function App() {
  const [document, setDocument] = useState(null)
  const [sessionId, setSessionId] = useState('')
  const [busy, setBusy] = useState('')
  const [error, setError] = useState('')
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [dragging, setDragging] = useState(false)
  const [activeSource, setActiveSource] = useState(null)
  const inputRef = useRef(null)
  const fileRef = useRef(null)
  const ready = Boolean(sessionId)

  async function processFile(file) {
    if (!file) return
    setError('')
    if (!file.name.toLowerCase().endsWith('.pdf')) return setError('Please choose a PDF document.')
    setBusy('upload')
    setDocument({ name: file.name, size: file.size, status: 'processing' })
    setSessionId('')
    setMessages([])
    const form = new FormData()
    form.append('file', file)
    try {
      const result = await api('/api/documents', { method: 'POST', body: form })
      setSessionId(result.session_id)
      setDocument({ ...result, size: file.size, status: 'ready' })
    } catch (err) {
      setDocument(null)
      setError(err.message)
    } finally { setBusy('') }
  }

  async function loadDemo() {
    setError(''); setBusy('upload')
    try {
      const result = await api('/api/demo', { method: 'POST' })
      setSessionId(result.session_id); setDocument({ ...result, size: null, status: 'ready' }); setMessages([])
    } catch (err) { setError(err.message) }
    finally { setBusy('') }
  }

  async function clearDocument() {
    if (sessionId) api(`/api/sessions/${sessionId}`, { method: 'DELETE' }).catch(() => {})
    setDocument(null); setSessionId(''); setMessages([]); setError(''); setActiveSource(null)
    if (fileRef.current) fileRef.current.value = ''
  }

  async function ask(text = question) {
    const value = text.trim()
    if (!value || !ready || busy) return
    setError(''); setQuestion(''); setMessages(current => [...current, { role: 'user', text: value }]); setBusy('answer')
    try {
      const result = await api(`/api/sessions/${sessionId}/questions`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: value }) })
      setMessages(current => [...current, { role: 'assistant', text: result.answer, sources: result.sources }])
    } catch (err) { setError(err.message) }
    finally { setBusy('') }
  }

  function submit(e) { e.preventDefault(); ask() }
  function formatSize(bytes) { return bytes ? `${(bytes / 1024 / 1024).toFixed(1)} MB` : 'Sample document' }

  return <div className="app-shell">
    <header className="topbar">
      <a className="brand" href="#" aria-label="LegalLens home"><span className="brand-mark"><Scale size={19} strokeWidth={2.2} /></span><span>legal<span className="brand-light">lens</span><i>AI</i></span></a>
      <div className="top-center"><span className="status-dot" /> Private workspace</div>
      <div className="top-right"><span className="top-label">Built for clarity</span><div className="avatar">L</div></div>
    </header>

    <main className="workspace">
      <aside className="sidebar">
        <div className="sidebar-heading"><span>WORKSPACE</span><button title="New conversation" onClick={clearDocument}><Plus size={16} /></button></div>
        <button className={`nav-item ${!ready ? 'selected' : ''}`} onClick={() => { if (!ready) window.scrollTo({ top: 0, behavior: 'smooth' }) }}><MessageSquareText size={17} /><span>Document chat</span><span className="nav-count">01</span></button>
        <div className="side-divider" />
        <div className="sidebar-heading docs-heading"><span>YOUR DOCUMENT</span></div>
        {document ? <div className="side-document"><span className="pdf-icon"><FileText size={16} /></span><span className="side-doc-copy"><strong>{document.filename || document.name}</strong><small>{document.status === 'ready' ? `${document.pages} pages · Ready` : 'Processing…'}</small></span><button onClick={clearDocument} aria-label="Remove document"><X size={14} /></button></div> : <div className="side-empty">Your documents will appear here.</div>}
        <div className="sidebar-bottom"><div className="shield-row"><ShieldCheck size={17} /><span>Your documents stay private</span></div><p>Answers are grounded in your source material.</p></div>
      </aside>

      <section className="main-panel">
        <div className="content-wrap">
          <div className="breadcrumb"><span>Workspace</span><span className="crumb-slash">/</span><strong>Document chat</strong><span className="beta-tag">BETA</span></div>
          <div className="intro-row"><div><div className="eyebrow"><Sparkles size={14} /> LEGAL DOCUMENT INTELLIGENCE</div><h1>Clarity in every <span>clause.</span></h1><p className="intro-copy">Ask your documents anything. Get grounded answers with sources you can trust.</p></div><div className="intro-stamp"><Gavel size={24} /><span>READ THE<br/>FINE PRINT</span></div></div>

          {!ready ? <section className="upload-card">
            <div className={`drop-zone ${dragging ? 'drag-active' : ''} ${busy === 'upload' ? 'is-processing' : ''}`} onDragOver={e => { e.preventDefault(); setDragging(true) }} onDragLeave={() => setDragging(false)} onDrop={e => { e.preventDefault(); setDragging(false); processFile(e.dataTransfer.files?.[0]) }} onClick={() => !busy && fileRef.current?.click()} role="button" tabIndex={0} onKeyDown={e => e.key === 'Enter' && fileRef.current?.click()}>
              <input ref={fileRef} type="file" accept="application/pdf,.pdf" hidden onChange={e => processFile(e.target.files?.[0])} />
              <div className="upload-icon">{busy === 'upload' ? <LoaderCircle className="spin" size={23} /> : <FileUp size={23} />}</div>
              <h2>{busy === 'upload' ? 'Reading your document…' : 'Start with a document'}</h2>
              <p>{busy === 'upload' ? 'Extracting pages and preparing your private workspace.' : <>Drag and drop a PDF here, or <span className="browse-link">browse files</span></>}</p>
              {!busy && <span className="file-limit">PDF · UP TO 25 MB</span>}
              {busy === 'upload' && <div className="progress-track"><span /></div>}
            </div>
            <div className="upload-footer"><div className="secure-note"><ShieldCheck size={16} /><span>Encrypted in transit · Your files are never used to train models</span></div><button className="sample-btn" onClick={loadDemo} disabled={Boolean(busy)}><FileText size={15} /> Try a sample agreement <ArrowRight size={14} /></button></div>
            {error && <div className="error-banner"><X size={16} />{error}</div>}
          </section> : <>
            <div className="ready-banner"><div className="ready-left"><div className="ready-check"><Check size={16} /></div><div><strong>Document ready</strong><span>Your file has been indexed and is ready for questions.</span></div></div><div className="ready-meta"><span><FileText size={15} /> {document.filename}</span><span className="meta-sep">·</span><span>{document.pages} pages</span><button onClick={clearDocument} title="Remove document"><X size={15} /></button></div></div>
            <div className={`chat-area ${messages.length ? 'has-messages' : ''}`}>
              {!messages.length ? <div className="welcome-chat"><div className="welcome-icon"><Sparkles size={19} /></div><span className="welcome-label">YOUR DOCUMENT, MADE CLEAR</span><h2>What would you like<br/>to understand?</h2><p>Ask a question or choose a place to start.</p><div className="suggestions">{suggestions.map(({ icon: Icon, text }) => <button key={text} onClick={() => ask(text)} disabled={Boolean(busy)}><Icon size={16} /><span>{text}</span><ArrowRight size={14} className="suggest-arrow" /></button>)}</div></div> : <div className="messages">{messages.map((message, i) => <div className={`message ${message.role}`} key={i}>{message.role === 'assistant' && <div className="assistant-avatar"><Scale size={15} /></div>}<div className="message-body"><span className="message-author">{message.role === 'user' ? 'YOU' : 'LEGALLENS'}</span><div className="message-text">{message.text}</div>{message.sources?.length > 0 && <div className="sources"><button className="sources-toggle" onClick={() => setActiveSource(activeSource === i ? null : i)}><BookOpen size={14} /> {message.sources.length} sources <ChevronDown size={14} className={activeSource === i ? 'rotated' : ''} /></button>{activeSource === i && <div className="source-list">{message.sources.map((source, n) => <div className="source-card" key={n}><span className="source-page">PAGE {source.page_number}</span><p>{source.text}</p></div>)}</div>}</div>}</div></div>)}{busy === 'answer' && <div className="message assistant"><div className="assistant-avatar"><Scale size={15} /></div><div className="message-body"><span className="message-author">LEGALLENS</span><div className="typing"><i/><i/><i/></div></div></div>}<div ref={el => el?.scrollIntoView({ behavior: 'smooth', block: 'end' })} /></div>}
            </div>
            {error && <div className="error-banner chat-error"><X size={16} />{error}<button onClick={() => setError('')}><X size={14}/></button></div>}
            <form className="composer" onSubmit={submit}><div className="composer-top"><textarea ref={inputRef} value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask() } }} placeholder="Ask a question about your document…" rows="1" disabled={Boolean(busy)} /><button className="send-btn" type="submit" disabled={!question.trim() || Boolean(busy)} aria-label="Send question">{busy === 'answer' ? <LoaderCircle size={17} className="spin"/> : <ArrowUp size={18}/>}</button></div><div className="composer-bottom"><span><ShieldCheck size={13} /> Answers cite your document</span><span>↵ Send <i>·</i> ⇧↵ New line</span></div></form>
          </>}

          <footer className="page-footer"><span><BadgeCheck size={14} /> Designed for careful reading</span><span>LegalLens AI · Informational use only</span></footer>
        </div>
      </section>
    </main>
  </div>
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>)
