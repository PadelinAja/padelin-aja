# Padelin Aja 

## 📖 Description
Padel has rapidly become one of the fastest-growing sports in Indonesia, attracting players of all ages and backgrounds. In recent years, the sport has seen a surge of popularity in major cities across Java, especially within the Jabodetabek area (Jakarta, Bogor, Depok, Tangerang, and Bekasi). Despite this growing enthusiasm, there remains a lack of centralized information for players who want to find venues, join matches, or connect with the local padel community.

**Padelin Aja** is developed as a solution to that problem. It is a community-driven web platform designed to serve as an integrated hub for padel enthusiasts in Indonesia. The website combines a comprehensive venue directory, an events listing system, and a community content section that features articles and news about the sport. The main goal of this platform is to promote the growth of padel in Indonesia by connecting players, organizers, and venue owners through a single, user-friendly platform.

Through Padelin Aja, users can explore padel venues across Java, read community articles, and stay updated about ongoing or upcoming tournaments and fun matches. The platform allows users to filter venues by city, view detailed contact information (address, phone number, social media, or website), and engage with the community by posting comments or sharing experiences. Registered users can also manage their profiles, save favorite venues, and participate in discussions around events or articles. 

From a technical perspective, **Padelin Aja** is built using the **Django Framework** with the Model–View–Template (MVT) architecture. Each component of the website is implemented as a distinct module, allowing collaborative development and easier integration. Django’s structure enables clear separation between data models, server logic, and HTML templates, resulting in a maintainable and scalable system. The website also applies responsive web design principles, ensuring accessibility across devices and screen sizes.

Additional features include:
- **Responsive Design** using CSS frameworks such as Bootstrap or TailwindCSS for mobile-friendly layouts.
- **AJAX integration** for dynamic user interactions such as commenting without requiring full page reloads.
- **Role-based user system** that differentiates permissions between guests, members, and administrators.
- **Dataset integration** using a curated dataset of more than 100 padel venues and related community data from trusted online sources and manual collection.

Ultimately, **Padelin Aja** is not just a sports information portal, but a digital ecosystem that supports the development of the padel community in Indonesia. It is designed to make local padel information more accessible, help new players find suitable venues and events, and strengthen connections between players and organizers. Through this project, the team hopes to contribute to the visibility and growth of padel as a mainstream sport within the Indonesian sporting landscape.

---

## 📊 Dataset Source
The initial dataset (≥100 entries) will focus on **Padel venues and related community information** in Java.  
Data sources:
- [https://docs.google.com/spreadsheets/d/12ymaAbHhamWzBvRnOXEskvQe60PCF-trpwEMifoZLBo/edit?usp=sharing] - Our team Google Sheets for the dataset
- [Ayo.co.id Blog](https://ayo.co.id/blog) – articles and venue information related to padel.  

---

## 👥 Group Members
- Member 1 – Davin Muhammad Hijran (2406365244)
- Member 2 – Bagas Zharif Prasetyo (2406453423)
- Member 3 – Roben Joseph Buce Tambayong (2406453594)
- Member 4 – Herdayani Elision Sitio (2406365313) 
- Member 5 – Radithya Naufal Mulia (2406365225)

---

## 🧩 Modules
Each group member is responsible for one module:

1. **Venues Directory**  (Roben)
   - Model: Venue (name, city, address, contact, website/socials).  
   - Features: List + filter by city, search by name.   

2. **User Profiles & Authentication**  (Bagas)
   - User registration/login system.  
   - Profile page with saved/bookmarked venues.  

3. **Articles/News**  (Davin)
   - Model: Article (title, content, cateory, author, date).  
   - Features: Article listing + detail page.

4. **Comments & Community Interaction**  (Elision)
   - AJAX-based commenting system for articles/venues.  

5. **Events (Fun Match & Tournament)**  (Radith)
   - Model: Event (name, date, location, description).  
   - Features: Show upcoming padel events in Java island.  

---

## 👥 User Roles
- **Guest**: Can comment and give rating on articles, venues.
- **Owner/Author**: Can add/edit/delete own venues, add/edit/delete own articles, and add/edit/delete own fun match.
- **Admin**: Can add/edit/delete all venues, add/edit/delete all articles, add/edit/delete tournament, and moderate content.  

---

## 🚀 Deployment
- **PWS Deployment Link**: *https://pbp.cs.ui.ac.id/roben.joseph/padelinaja*  

---

## 🎨 Design Framework
- **Figma Design Link**: *https://www.figma.com/design/xFBIqDvxI7vpdOzg797Bpq/PadelinAja?node-id=0-1&t=mNJyioSrtGSJRorF-1*

---
