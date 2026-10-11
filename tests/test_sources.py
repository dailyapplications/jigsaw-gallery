from tools.gallery.sources import cleveland, met, nasa, smk


def met_obj(**kw):
    o = {"objectID": 1, "isPublicDomain": True, "primaryImage": "https://i/1.jpg", "primaryImageSmall": "https://i/1s.jpg",
         "title": "Wheat Field", "artistDisplayName": "Vincent van Gogh", "artistEndDate": "1890",
         "objectDate": "1889", "objectEndDate": "1889", "classification": "Paintings", "objectURL": "https://met/1"}
    o.update(kw)
    return o


def test_met_accepts_public_domain_painting():
    c = met.candidate(met_obj())
    assert c.license == "CC0" and c.death_year == 1890 and c.year == 1889 and c.proof["isPublicDomain"]


def test_met_rejects_non_public_domain_missing_image_and_sculpture():
    assert met.candidate(met_obj(isPublicDomain=False)) is None
    assert met.candidate(met_obj(primaryImage="")) is None
    assert met.candidate(met_obj(classification="Sculpture")) is None


def test_met_unknown_artist_has_no_death_year():
    c = met.candidate(met_obj(artistDisplayName="", artistEndDate=""))
    assert c.creator == "Unknown artist" and c.death_year is None


def cle_row(**kw):
    r = {"id": 5, "title": "Swallows", "share_license_status": "CC0", "type": "Painting", "creation_date_latest": 1880,
         "images": {"print": {"url": "https://c/p.jpg"}, "web": {"url": "https://c/w.jpg"}},
         "creators": [{"description": "Claude Monet (French, 1840-1926)", "role": "artist", "death_year": "1926"}],
         "url": "https://cma/5"}
    r.update(kw)
    return r


def test_cleveland_accepts_cc0_painting():
    c = cleveland.candidate(cle_row())
    assert c.creator == "Claude Monet" and c.death_year == 1926


def test_cleveland_rejects_non_cc0_sculpture_and_no_image():
    assert cleveland.candidate(cle_row(share_license_status="Copyrighted")) is None
    assert cleveland.candidate(cle_row(type="Sculpture")) is None
    assert cleveland.candidate(cle_row(images={})) is None


def smk_row(**kw):
    r = {"object_number": "KMS1", "public_domain": True, "rights": "https://creativecommons.org/publicdomain/mark/1.0/",
         "image_native": "https://s/n.jpg", "image_thumbnail": "https://s/t.jpg", "object_names": [{"name": "Maleri"}],
         "production": [{"creator_forename": "Anna", "creator_surname": "Ancher", "creator_date_of_death": "1935-04-15T00:00:00.000Z"}],
         "production_date": [{"end": "1903-12-31T00:00:00.000Z"}],
         "titles": [{"title": "Sunlight", "language": "engelsk"}]}
    r.update(kw)
    return r


def test_smk_accepts_public_domain_painting_with_english_title():
    c = smk.candidate(smk_row())
    assert c.title == "Sunlight" and c.creator == "Anna Ancher" and c.death_year == 1935 and c.year == 1903


def test_smk_rejects_not_public_domain_or_other_rights_or_object_types():
    assert smk.candidate(smk_row(public_domain=False)) is None
    assert smk.candidate(smk_row(rights="https://rightsstatements.org/vocab/InC/1.0/")) is None
    assert smk.candidate(smk_row(object_names=[{"name": "Skulptur"}])) is None


def nasa_item(**kw):
    d = {"media_type": "image", "nasa_id": "PIA1", "title": "Orion", "center": "JPL", "date_created": "2011-08-10T21:00:09Z"}
    d.update(kw)
    return {"data": [d], "links": [{"href": "https://n/thumb.jpg"}]}


def test_nasa_accepts_nasa_created_image_only():
    assert nasa.candidate(nasa_item()).license == "NASA"
    assert nasa.candidate(nasa_item(secondary_creator="Some Photographer")) is None
    assert nasa.candidate(nasa_item(center="Unknown Agency")) is None
    assert nasa.candidate(nasa_item(media_type="video")) is None
