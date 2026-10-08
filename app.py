import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

st.set_page_config(page_title="AI Multi-Agent Writer", page_icon="🤖")

st.title("🤖 AI Multi-Agent Content Generator")
st.write("Aplikasi kolaborasi AI Agent (Peneliti & Penulis) menggunakan CrewAI dan Gemini.")

# Input API Key dari pengguna (atau bisa disembunyikan jika pakai secrets)
api_key_input = st.text_input("Masukkan Google Gemini API Key Anda:", type="password")

topik = st.text_input("Masukkan topik yang ingin dibahas:", "Perkembangan AI Agent di Dunia Pendidikan")

if st.button("🚀 Jalankan Agen"):
    if not api_key_input:
        st.error("Mohon masukkan API Key terlebih dahulu!")
    else:
        with st.spinner("🤖 Agen sedang bekerja meneliti dan menulis... Mohon tunggu sebentar."):
            try:
                # Set Environment
                os.environ["GEMINI_API_KEY"] = api_key_input
                os.environ["GOOGLE_API_KEY"] = api_key_input
                
                llm = LLM(model="gemini/gemini-1.5-flash", api_key=api_key_input)
                
                # Definisikan Agen
                researcher = Agent(
                    role='Senior Researcher',
                    goal=f'Mencari informasi mendalam mengenai: {topik}',
                    backstory='Peneliti yang teliti dan cepat.',
                    llm=llm,
                    verbose=False
                )
                
                writer = Agent(
                    role='Tech Writer',
                    goal='Menulis artikel menarik berdasarkan hasil riset.',
                    backstory='Penulis konten profesional.',
                    llm=llm,
                    verbose=False
                )
                
                # Tasks
                task1 = Task(
                    description=f'Cari 3 poin penting tentang {topik}',
                    expected_output='Daftar 3 poin penting.',
                    agent=researcher
                )
                
                task2 = Task(
                    description='Tulis artikel pendek berdasarkan hasil riset.',
                    expected_output='Artikel singkat yang rapi.',
                    agent=writer
                )
                
                crew = Crew(
                    agents=[researcher, writer],
                    tasks=[task1, task2],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                
                st.success("Selesai!")
                st.markdown("### Hasil Artikel:")
                st.write(str(result))
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
